import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

import openai
from fastapi import HTTPException
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather

# Import quantum components
sys.path.append('../../core')
from quantum_job_manager import QuantumJobManager, QUBOBuilder
from qdllm_service import QdLLMService
from qhc_governance import QHCGovernance
from mcp_integration import MCPProvider

class CallStatus(Enum):
    """Call status enumeration"""
    INITIATED = "initiated"
    RINGING = "ringing"
    ANSWERED = "answered"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    TRANSFERRED = "transferred"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
    CANCELLED = "cancelled"

class CallType(Enum):
    """Types of calls"""
    OUTBOUND_SALES = "outbound_sales"
    INBOUND_SUPPORT = "inbound_support"
    FOLLOW_UP = "follow_up"
    APPOINTMENT = "appointment"
    SURVEY = "survey"
    NOTIFICATION = "notification"

@dataclass
class CallSession:
    """Active call session data"""
    call_id: str
    session_id: str
    phone_number: str
    lead_id: Optional[str]
    script_id: Optional[str]
    call_type: CallType
    status: CallStatus
    started_at: datetime
    ended_at: Optional[datetime]
    transcript: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    consent_given: bool = False
    recording_enabled: bool = False
    
class QuantumCallingAgent:
    """Quantum-enhanced calling agent with real-time STT/TTS and TCPA compliance"""
    
    def __init__(self,
                 agent_id: str,
                 quantum_job_manager: QuantumJobManager,
                 qdllm_service: QdLLMService,
                 qhc_governance: QHCGovernance,
                 mcp_provider: MCPProvider,
                 twilio_client: TwilioClient,
                 openai_client: openai.AsyncOpenAI = None):
        self.agent_id = agent_id
        self.quantum_job_manager = quantum_job_manager
        self.qdllm_service = qdllm_service
        self.qhc_governance = qhc_governance
        self.mcp_provider = mcp_provider
        self.twilio_client = twilio_client
        self.openai_client = openai_client
        self.logger = logging.getLogger(f"quantum_calling_agent_{agent_id}")
        
        # Active call sessions
        self.active_calls: Dict[str, CallSession] = {}
        
        # Do-not-call registry
        self.dnc_registry: set = set()
        
        # Call scripts and flows
        self.call_scripts: Dict[str, Dict] = {}
        
        # Agent capabilities
        self.capabilities = {
            "real_time_stt": True,
            "quantum_tts": True,
            "tcpa_compliance": True,
            "call_recording": True,
            "sentiment_analysis": True,
            "objection_handling": True,
            "escalation_management": True
        }
        
    async def initialize(self):
        """Initialize calling agent and register with MCP"""
        
        # Load do-not-call registry
        await self._load_dnc_registry()
        
        # Load call scripts
        await self._load_call_scripts()
        
        # Register with MCP
        await self.mcp_provider.register_agent({
            "agent_id": self.agent_id,
            "type": "quantum_calling_agent",
            "capabilities": self.capabilities,
            "endpoints": [
                "/api/agents/{id}/call-start",
                "/api/agents/{id}/call-handoff",
                "/api/agents/{id}/postcall-summary",
                "/api/agents/{id}/call-status",
                "/api/agents/{id}/update-script"
            ]
        })
        
        self.logger.info(f"Quantum Calling Agent {self.agent_id} initialized")
        
    async def start_call(self,
                        phone: str,
                        lead_id: str = None,
                        script_id: str = None,
                        call_type: CallType = CallType.OUTBOUND_SALES,
                        metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Initiate outbound call with TCPA compliance"""
        
        try:
            # TCPA compliance checks
            compliance_check = await self._check_tcpa_compliance(phone, call_type, metadata)
            if not compliance_check["compliant"]:
                raise HTTPException(
                    status_code=403, 
                    detail=f"TCPA violation: {compliance_check['reason']}"
                )
                
            # Generate call session
            call_id = str(uuid.uuid4())
            session_id = str(uuid.uuid4())
            
            call_session = CallSession(
                call_id=call_id,
                session_id=session_id,
                phone_number=phone,
                lead_id=lead_id,
                script_id=script_id,
                call_type=call_type,
                status=CallStatus.INITIATED,
                started_at=datetime.utcnow(),
                ended_at=None,
                transcript=[],
                metadata=metadata or {},
                consent_given=False,
                recording_enabled=False
            )
            
            self.active_calls[call_id] = call_session
            
            # Get QHC approval for call
            qhc_approval = await self.qhc_governance.approve_call({
                "call_id": call_id,
                "phone": phone,
                "lead_id": lead_id,
                "call_type": call_type.value,
                "agent_id": self.agent_id
            })
            
            if not qhc_approval["approved"]:
                call_session.status = CallStatus.CANCELLED
                raise HTTPException(
                    status_code=403,
                    detail=f"Call not approved: {qhc_approval['reason']}"
                )
                
            # Initiate Twilio call
            twilio_call = self.twilio_client.calls.create(
                to=phone,
                from_=self._get_caller_id(call_type),
                url=f"{self._get_webhook_base_url()}/voice/handle/{call_id}",
                status_callback=f"{self._get_webhook_base_url()}/voice/status/{call_id}",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
                record=False,  # Will enable after consent
                timeout=30
            )
            
            call_session.metadata["twilio_call_sid"] = twilio_call.sid
            call_session.status = CallStatus.RINGING
            
            self.logger.info(f"Call {call_id} initiated to {phone}")
            
            return {
                "call_id": call_id,
                "session_id": session_id,
                "status": call_session.status.value,
                "twilio_call_sid": twilio_call.sid,
                "estimated_wait_time": "30 seconds",
                "compliance_verified": True
            }
            
        except Exception as e:
            self.logger.error(f"Failed to start call to {phone}: {e}")
            if call_id in self.active_calls:
                self.active_calls[call_id].status = CallStatus.FAILED
            raise
            
    async def handle_voice_webhook(self, call_id: str, request_data: Dict) -> str:
        """Handle Twilio voice webhook for call flow"""
        
        call_session = self.active_calls.get(call_id)
        if not call_session:
            return self._generate_error_twiml("Call session not found")
            
        try:
            # Update call status
            if request_data.get("CallStatus") == "answered":
                call_session.status = CallStatus.ANSWERED
                
            # Generate initial response based on script
            script = self.call_scripts.get(call_session.script_id, self._get_default_script())
            
            # Use quantum-enhanced conversation flow
            flow_decision = await self._determine_conversation_flow(call_session, request_data)
            
            # Generate TwiML response
            twiml_response = await self._generate_twiml_response(call_session, flow_decision)
            
            return str(twiml_response)
            
        except Exception as e:
            self.logger.error(f"Voice webhook error for call {call_id}: {e}")
            return self._generate_error_twiml("Processing error occurred")
            
    async def handle_speech_input(self, call_id: str, speech_result: Dict) -> str:
        """Process speech input and generate response"""
        
        call_session = self.active_calls.get(call_id)
        if not call_session:
            return self._generate_error_twiml("Call session not found")
            
        try:
            # Extract speech text
            speech_text = speech_result.get("SpeechResult", "")
            confidence = float(speech_result.get("Confidence", 0.0))
            
            # Add to transcript
            transcript_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "speaker": "caller",
                "text": speech_text,
                "confidence": confidence,
                "metadata": speech_result
            }
            call_session.transcript.append(transcript_entry)
            
            # Process with quantum-enhanced reasoning
            response_data = await self._process_caller_input(
                call_session, speech_text, confidence
            )
            
            # Generate TTS response
            tts_response = await self._generate_tts_response(
                call_session, response_data["response_text"]
            )
            
            # Add agent response to transcript
            agent_transcript = {
                "timestamp": datetime.utcnow().isoformat(),
                "speaker": "agent",
                "text": response_data["response_text"],
                "confidence": response_data["confidence"],
                "intent": response_data.get("intent"),
                "sentiment": response_data.get("sentiment")
            }
            call_session.transcript.append(agent_transcript)
            
            # Generate TwiML with response
            response = VoiceResponse()
            
            # Check if escalation is needed
            if response_data.get("escalation_recommended"):
                return await self._handle_escalation_twiml(call_session, response_data)
                
            # Add TTS
            response.say(tts_response["audio_text"], voice="alice", language="en-US")
            
            # Continue conversation or end call
            if response_data.get("continue_conversation", True):
                gather = Gather(
                    input="speech",
                    timeout=10,
                    speech_timeout="auto",
                    action=f"/voice/speech/{call_id}",
                    method="POST"
                )
                response.append(gather)
                
                # Fallback if no speech detected
                response.say("I didn't hear anything. Please speak now or press any key.")
                response.redirect(f"/voice/handle/{call_id}")
            else:
                # End call
                response.say("Thank you for your time. Have a great day!")
                response.hangup()
                call_session.status = CallStatus.COMPLETED
                call_session.ended_at = datetime.utcnow()
                
            return str(response)
            
        except Exception as e:
            self.logger.error(f"Speech processing error for call {call_id}: {e}")
            return self._generate_error_twiml("I'm sorry, I didn't understand that. Could you repeat?")
            
    async def _process_caller_input(self, 
                                   call_session: CallSession,
                                   speech_text: str,
                                   confidence: float) -> Dict[str, Any]:
        """Process caller input with quantum-enhanced reasoning"""
        
        # Build conversation context
        context = {
            "call_type": call_session.call_type.value,
            "transcript_history": call_session.transcript[-5:],  # Last 5 exchanges
            "lead_id": call_session.lead_id,
            "call_duration": (datetime.utcnow() - call_session.started_at).total_seconds(),
            "consent_given": call_session.consent_given
        }
        
        # Use qdLLM for intent analysis and response generation
        analysis_prompt = self._build_caller_analysis_prompt(speech_text, context)
        
        analysis_result = await self.qdllm_service.generate(
            prompt=analysis_prompt,
            max_tokens=400,
            temperature=0.7,
            quantum_enhanced=True
        )
        
        # Extract analysis results
        intent = analysis_result.get("intent", "unknown")
        sentiment = analysis_result.get("sentiment", "neutral")
        objections = analysis_result.get("objections", [])
        
        # Generate response candidates
        response_candidates = await self._generate_response_candidates(
            call_session, speech_text, intent, sentiment, objections
        )
        
        # Use QUBO to select optimal response
        optimal_response = await self._select_optimal_call_response(
            response_candidates, call_session, context
        )
        
        # Check for escalation triggers
        escalation_check = await self._check_escalation_triggers(
            call_session, speech_text, intent, sentiment
        )
        
        return {
            "response_text": optimal_response["content"],
            "confidence": optimal_response["confidence"],
            "intent": intent,
            "sentiment": sentiment,
            "objections_detected": objections,
            "escalation_recommended": escalation_check["escalate"],
            "escalation_reason": escalation_check.get("reason"),
            "continue_conversation": optimal_response.get("continue_conversation", True),
            "suggested_actions": optimal_response.get("actions", [])
        }
        
    async def _generate_response_candidates(self,
                                          call_session: CallSession,
                                          speech_text: str,
                                          intent: str,
                                          sentiment: str,
                                          objections: List[str]) -> List[Dict[str, Any]]:
        """Generate multiple response candidates for QUBO selection"""
        
        candidates = []
        
        # Strategy-based response generation
        strategies = [
            "direct_response",
            "empathetic_acknowledgment",
            "value_reinforcement",
            "objection_handling",
            "information_gathering"
        ]
        
        # Add call-type specific strategies
        if call_session.call_type == CallType.OUTBOUND_SALES:
            strategies.extend(["benefit_highlighting", "urgency_creation"])
        elif call_session.call_type == CallType.INBOUND_SUPPORT:
            strategies.extend(["problem_solving", "reassurance"])
            
        # Generate candidates in parallel
        tasks = []
        for strategy in strategies[:5]:  # Limit to 5 candidates
            task = self._generate_strategy_call_response(
                call_session, speech_text, intent, sentiment, objections, strategy
            )
            tasks.append(task)
            
        candidate_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(candidate_results):
            if not isinstance(result, Exception) and result:
                candidates.append({
                    "id": f"candidate_{i}",
                    "strategy": strategies[i],
                    "content": result["content"],
                    "confidence": result.get("confidence", 0.5),
                    "continue_conversation": result.get("continue_conversation", True),
                    "metadata": result.get("metadata", {})
                })
                
        return candidates
        
    async def _generate_strategy_call_response(self,
                                             call_session: CallSession,
                                             speech_text: str,
                                             intent: str,
                                             sentiment: str,
                                             objections: List[str],
                                             strategy: str) -> Dict[str, Any]:
        """Generate response for specific strategy"""
        
        prompt = self._build_call_strategy_prompt(
            call_session, speech_text, intent, sentiment, objections, strategy
        )
        
        result = await self.qdllm_service.generate(
            prompt=prompt,
            max_tokens=200,  # Shorter for phone conversations
            temperature=0.8 if strategy == "empathetic_acknowledgment" else 0.6,
            quantum_enhanced=True
        )
        
        return {
            "content": result.get("response", ""),
            "confidence": result.get("confidence", 0.5),
            "continue_conversation": result.get("continue_conversation", True),
            "metadata": {
                "strategy": strategy,
                "estimated_effectiveness": result.get("effectiveness", 0.5),
                "tone": result.get("tone", "professional")
            }
        }
        
    async def _select_optimal_call_response(self,
                                          candidates: List[Dict[str, Any]],
                                          call_session: CallSession,
                                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Use QUBO to select optimal call response"""
        
        if not candidates:
            return self._get_fallback_call_response(call_session)
            
        # Score candidates for call context
        weights = {
            "confidence": 0.25,
            "appropriateness": 0.25,
            "persuasiveness": 0.2,
            "clarity": 0.15,
            "brevity": 0.15  # Important for phone calls
        }
        
        # Score candidates
        scored_candidates = []
        for candidate in candidates:
            scores = await self._score_call_candidate(candidate, call_session, context)
            scored_candidates.append({
                **candidate,
                "scores": scores
            })
            
        # Build QUBO matrix
        qubo_matrix = QUBOBuilder.build_ranking_qubo(scored_candidates, weights)
        
        # Submit to quantum job manager
        qubo_result = await self.quantum_job_manager.submit_qubo(
            problem_matrix=qubo_matrix,
            job_metadata={
                "agent_id": self.agent_id,
                "task": "call_response_selection",
                "call_id": call_session.call_id,
                "call_type": call_session.call_type.value
            }
        )
        
        # Extract selected candidate
        solution = qubo_result.get("solution", {})
        selected_idx = max(solution.keys(), key=lambda k: solution[k]) if solution else 0
        
        if selected_idx < len(scored_candidates):
            selected = scored_candidates[selected_idx]
            selected["selection_metadata"] = {
                "qubo_energy": qubo_result.get("energy"),
                "quantum_optimized": True
            }
            return selected
        else:
            return max(scored_candidates, key=lambda c: c["confidence"])
            
    async def handoff_to_human(self,
                              call_id: str,
                              human_agent_id: str,
                              reason: str = None) -> Dict[str, Any]:
        """Hand off call to human agent"""
        
        call_session = self.active_calls.get(call_id)
        if not call_session:
            raise HTTPException(status_code=404, detail="Call session not found")
            
        try:
            # Generate handoff summary
            handoff_summary = await self._generate_handoff_summary(call_session)
            
            # Get QHC approval for handoff
            handoff_request = {
                "call_id": call_id,
                "human_agent_id": human_agent_id,
                "reason": reason,
                "call_summary": handoff_summary,
                "agent_id": self.agent_id
            }
            
            qhc_approval = await self.qhc_governance.approve_handoff(handoff_request)
            
            if qhc_approval["approved"]:
                # Update call status
                call_session.status = CallStatus.TRANSFERRED
                call_session.metadata["transferred_to"] = human_agent_id
                call_session.metadata["transfer_reason"] = reason
                call_session.metadata["transfer_time"] = datetime.utcnow().isoformat()
                
                # Create handoff record
                handoff_id = str(uuid.uuid4())
                
                handoff_record = {
                    "handoff_id": handoff_id,
                    "call_id": call_id,
                    "from_agent": self.agent_id,
                    "to_agent": human_agent_id,
                    "reason": reason,
                    "timestamp": datetime.utcnow().isoformat(),
                    "call_summary": handoff_summary,
                    "transcript": call_session.transcript,
                    "recommendations": qhc_approval.get("recommendations", [])
                }
                
                # Store handoff record
                await self._store_handoff_record(handoff_record)
                
                return {
                    "handoff_id": handoff_id,
                    "status": "approved",
                    "human_agent_id": human_agent_id,
                    "call_summary": handoff_summary,
                    "recommendations": handoff_record["recommendations"],
                    "estimated_transfer_time": "30 seconds"
                }
            else:
                return {
                    "status": "denied",
                    "reason": qhc_approval.get("denial_reason"),
                    "alternatives": qhc_approval.get("alternatives", [])
                }
                
        except Exception as e:
            self.logger.error(f"Handoff error for call {call_id}: {e}")
            raise HTTPException(status_code=500, detail="Handoff processing failed")
            
    async def generate_postcall_summary(self, call_id: str) -> Dict[str, Any]:
        """Generate comprehensive post-call summary"""
        
        call_session = self.active_calls.get(call_id)
        if not call_session:
            raise HTTPException(status_code=404, detail="Call session not found")
            
        try:
            # Calculate call metrics
            call_duration = (call_session.ended_at or datetime.utcnow()) - call_session.started_at
            
            # Analyze conversation
            conversation_analysis = await self._analyze_full_conversation(call_session)
            
            # Generate summary using qdLLM
            summary_prompt = self._build_postcall_summary_prompt(call_session, conversation_analysis)
            
            summary_result = await self.qdllm_service.generate(
                prompt=summary_prompt,
                max_tokens=600,
                temperature=0.3,  # Lower temperature for factual summary
                quantum_enhanced=False
            )
            
            # Extract key outcomes
            outcomes = await self._extract_call_outcomes(call_session, conversation_analysis)
            
            # Generate follow-up recommendations
            follow_up_recommendations = await self._generate_followup_recommendations(
                call_session, conversation_analysis, outcomes
            )
            
            summary = {
                "call_id": call_id,
                "session_id": call_session.session_id,
                "call_details": {
                    "phone_number": call_session.phone_number,
                    "lead_id": call_session.lead_id,
                    "call_type": call_session.call_type.value,
                    "duration_seconds": int(call_duration.total_seconds()),
                    "status": call_session.status.value,
                    "started_at": call_session.started_at.isoformat(),
                    "ended_at": call_session.ended_at.isoformat() if call_session.ended_at else None
                },
                "conversation_summary": summary_result.get("summary", ""),
                "key_points": summary_result.get("key_points", []),
                "sentiment_analysis": conversation_analysis["overall_sentiment"],
                "objections_raised": conversation_analysis["objections"],
                "outcomes": outcomes,
                "follow_up_recommendations": follow_up_recommendations,
                "performance_metrics": {
                    "agent_talk_time_percentage": conversation_analysis["agent_talk_percentage"],
                    "customer_engagement_score": conversation_analysis["engagement_score"],
                    "call_quality_score": conversation_analysis["quality_score"],
                    "objection_handling_score": conversation_analysis["objection_handling_score"]
                },
                "compliance_notes": {
                    "consent_obtained": call_session.consent_given,
                    "recording_enabled": call_session.recording_enabled,
                    "tcpa_compliant": True,
                    "dnc_checked": True
                },
                "transcript": call_session.transcript,
                "metadata": call_session.metadata
            }
            
            # Store summary for analytics
            await self._store_call_summary(summary)
            
            # Clean up active call session
            if call_session.status in [CallStatus.COMPLETED, CallStatus.FAILED]:
                del self.active_calls[call_id]
                
            return summary
            
        except Exception as e:
            self.logger.error(f"Post-call summary error for {call_id}: {e}")
            raise HTTPException(status_code=500, detail="Summary generation failed")
            
    # TCPA Compliance Methods
    async def _check_tcpa_compliance(self, 
                                   phone: str, 
                                   call_type: CallType,
                                   metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check TCPA compliance before making call"""
        
        # Check do-not-call registry
        if phone in self.dnc_registry:
            return {
                "compliant": False,
                "reason": "Phone number is on do-not-call registry"
            }
            
        # Check time restrictions (9 AM - 8 PM local time)
        # This would need proper timezone handling in production
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour > 20:
            return {
                "compliant": False,
                "reason": "Call outside permitted hours (9 AM - 8 PM)"
            }
            
        # Check consent records
        consent_status = await self._check_consent_records(phone, call_type)
        if not consent_status["has_consent"]:
            return {
                "compliant": False,
                "reason": "No valid consent on file"
            }
            
        # Check call frequency limits
        recent_calls = await self._get_recent_calls(phone, days=30)
        if len(recent_calls) >= 3:  # Max 3 calls per month
            return {
                "compliant": False,
                "reason": "Exceeded call frequency limits"
            }
            
        return {
            "compliant": True,
            "consent_date": consent_status["consent_date"],
            "consent_type": consent_status["consent_type"]
        }
        
    # Helper methods for prompts and utilities
    def _build_caller_analysis_prompt(self, speech_text: str, context: Dict) -> str:
        """Build prompt for analyzing caller input"""
        
        return f"""
Analyze this caller input in a {context['call_type']} call:

Caller said: "{speech_text}"

Call context:
- Call duration: {context['call_duration']} seconds
- Consent given: {context['consent_given']}
- Recent conversation: {context['transcript_history'][-2:] if context['transcript_history'] else 'None'}

Provide analysis including:
1. Intent classification
2. Sentiment analysis
3. Objections detected
4. Engagement level
5. Response strategy recommendation

Respond in JSON format.
"""
        
    def _build_call_strategy_prompt(self, call_session: CallSession, speech_text: str,
                                   intent: str, sentiment: str, objections: List[str],
                                   strategy: str) -> str:
        """Build prompt for strategy-specific call response"""
        
        return f"""
Generate a {strategy} response for this phone conversation.

Call type: {call_session.call_type.value}
Caller input: "{speech_text}"
Detected intent: {intent}
Sentiment: {sentiment}
Objections: {objections}

Strategy guidelines:
{self._get_call_strategy_guidelines(strategy)}

Generate a brief, clear phone response (max 2 sentences).
Respond in JSON format with response, confidence, and continue_conversation flag.
"""
        
    def _get_call_strategy_guidelines(self, strategy: str) -> str:
        """Get guidelines for call response strategies"""
        
        guidelines = {
            "direct_response": "Provide clear, factual answer to the caller's question",
            "empathetic_acknowledgment": "Show understanding and validate caller's feelings",
            "value_reinforcement": "Highlight benefits and value proposition",
            "objection_handling": "Address concerns and overcome objections professionally",
            "information_gathering": "Ask relevant questions to better understand needs",
            "benefit_highlighting": "Emphasize key benefits and advantages",
            "urgency_creation": "Create appropriate sense of urgency",
            "problem_solving": "Focus on solving the caller's specific problem",
            "reassurance": "Provide comfort and confidence in the solution"
        }
        
        return guidelines.get(strategy, "Provide helpful and professional response")
        
    def _get_default_script(self) -> Dict:
        """Get default call script"""
        
        return {
            "opening": "Hello, this is [Agent Name] calling from [Company]. How are you today?",
            "consent_request": "I'd like to speak with you about [Topic]. Do I have your permission to continue?",
            "value_proposition": "I'm calling because we have a solution that could help you [Benefit].",
            "closing": "Thank you for your time today. Have a wonderful day!"
        }
        
    def _generate_error_twiml(self, message: str) -> str:
        """Generate error TwiML response"""
        
        response = VoiceResponse()
        response.say(message)
        response.hangup()
        return str(response)
        
    def _get_caller_id(self, call_type: CallType) -> str:
        """Get appropriate caller ID for call type"""
        
        # This would be configured based on call type and compliance requirements
        caller_ids = {
            CallType.OUTBOUND_SALES: "+1234567890",
            CallType.INBOUND_SUPPORT: "+1234567891",
            CallType.FOLLOW_UP: "+1234567892"
        }
        
        return caller_ids.get(call_type, "+1234567890")
        
    def _get_webhook_base_url(self) -> str:
        """Get base URL for webhooks"""
        # This would be configured in production
        return "https://your-domain.com/api/calling"
        
    # Additional utility methods would be implemented here...
    
    async def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """Get current call status"""
        
        call_session = self.active_calls.get(call_id)
        if not call_session:
            raise HTTPException(status_code=404, detail="Call not found")
            
        duration = (datetime.utcnow() - call_session.started_at).total_seconds()
        
        return {
            "call_id": call_id,
            "status": call_session.status.value,
            "duration_seconds": int(duration),
            "phone_number": call_session.phone_number,
            "call_type": call_session.call_type.value,
            "transcript_length": len(call_session.transcript),
            "consent_given": call_session.consent_given,
            "recording_enabled": call_session.recording_enabled
        }
        
    async def update_call_script(self, script_id: str, script_data: Dict) -> Dict[str, Any]:
        """Update call script"""
        
        self.call_scripts[script_id] = script_data
        
        return {
            "script_id": script_id,
            "updated": True,
            "timestamp": datetime.utcnow().isoformat()
        }

# Example usage
if __name__ == "__main__":
    async def test_calling_agent():
        # Initialize dependencies (mock implementations)
        quantum_job_manager = QuantumJobManager()
        qdllm_service = QdLLMService()
        qhc_governance = QHCGovernance()
        mcp_provider = MCPProvider()
        twilio_client = TwilioClient("account_sid", "auth_token")
        
        # Create agent
        agent = QuantumCallingAgent(
            agent_id="calling-001",
            quantum_job_manager=quantum_job_manager,
            qdllm_service=qdllm_service,
            qhc_governance=qhc_governance,
            mcp_provider=mcp_provider,
            twilio_client=twilio_client
        )
        
        await agent.initialize()
        
        # Test call initiation
        call_result = await agent.start_call(
            phone="+1234567890",
            lead_id="lead123",
            call_type=CallType.OUTBOUND_SALES
        )
        
        print(f"Call initiated: {call_result}")
        
    asyncio.run(test_calling_agent())