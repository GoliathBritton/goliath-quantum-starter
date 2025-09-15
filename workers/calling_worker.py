#!/usr/bin/env python3
"""
FLYFOX AI - Calling Worker
Handles outbound calling campaigns with AI-powered conversations.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

import aioredis
import asyncpg
import openai
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.base.exceptions import TwilioException
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallStatus(str, Enum):
    """Call status enumeration"""
    QUEUED = "queued"
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BUSY = "busy"
    NO_ANSWER = "no-answer"
    CANCELED = "canceled"
    BLOCKED = "blocked"

class CallOutcome(str, Enum):
    """Call outcome classification"""
    CONNECTED = "connected"
    VOICEMAIL = "voicemail"
    BUSY = "busy"
    NO_ANSWER = "no_answer"
    INVALID_NUMBER = "invalid_number"
    BLOCKED = "blocked"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    CALLBACK_REQUESTED = "callback_requested"
    OPTED_OUT = "opted_out"

@dataclass
class CallRecord:
    """Call record data structure"""
    id: str
    contact_id: str
    campaign_id: str
    phone_number: str
    status: CallStatus
    outcome: Optional[CallOutcome] = None
    duration: Optional[int] = None  # seconds
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    ai_summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    lead_score: Optional[int] = None
    next_action: Optional[str] = None
    scheduled_callback: Optional[datetime] = None
    twilio_call_sid: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

class AIConversationHandler:
    """Handles AI-powered conversation logic"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY')
        
    async def generate_opening_script(self, contact: Dict, campaign: Dict) -> str:
        """Generate personalized opening script"""
        try:
            prompt = f"""
            Generate a professional, personalized opening script for a business call.
            
            Contact Information:
            - Name: {contact.get('first_name', '')} {contact.get('last_name', '')}
            - Company: {contact.get('company', 'Unknown')}
            - Title: {contact.get('title', 'Unknown')}
            - Industry: {contact.get('industry', 'Unknown')}
            
            Campaign: {campaign.get('name', 'Business Outreach')}
            Purpose: {campaign.get('purpose', 'Introduce our AI automation solutions')}
            
            Requirements:
            - Keep it under 30 seconds
            - Be professional and respectful
            - Include compliance statement
            - Personalize based on contact info
            - Clear value proposition
            
            Format as a natural conversation starter.
            """
            
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional sales script writer specializing in B2B outreach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating opening script: {e}")
            return self._get_default_script(contact, campaign)
    
    def _get_default_script(self, contact: Dict, campaign: Dict) -> str:
        """Fallback default script"""
        name = contact.get('first_name', 'there')
        company = contact.get('company', 'your company')
        
        return f"""
        Hi {name}, this is calling from FlyFox AI regarding our automation solutions for {company}. 
        I have a quick question about your current workflow processes that might save you significant time. 
        Do you have 2 minutes to chat? This call may be recorded for quality purposes.
        """
    
    async def process_response(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Process user response and determine next action"""
        try:
            prompt = f"""
            Analyze this phone conversation response and determine the appropriate next action.
            
            User Response: "{user_input}"
            
            Context:
            - Call Purpose: {context.get('purpose', 'Business outreach')}
            - Stage: {context.get('stage', 'opening')}
            - Previous Responses: {context.get('history', [])}
            
            Analyze for:
            1. Sentiment (positive/neutral/negative)
            2. Interest level (high/medium/low/none)
            3. Intent (interested/not_interested/callback/more_info/opt_out)
            4. Next action (continue/schedule_callback/end_call/transfer)
            
            Return JSON format:
            {{
                "sentiment": "positive|neutral|negative",
                "interest_level": "high|medium|low|none",
                "intent": "interested|not_interested|callback|more_info|opt_out",
                "next_action": "continue|schedule_callback|end_call|transfer",
                "confidence": 0.0-1.0,
                "suggested_response": "What to say next",
                "lead_score": 1-10
            }}
            """
            
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert conversation analyst for sales calls. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error processing response: {e}")
            return {
                "sentiment": "neutral",
                "interest_level": "low",
                "intent": "not_interested",
                "next_action": "end_call",
                "confidence": 0.5,
                "suggested_response": "Thank you for your time. Have a great day!",
                "lead_score": 3
            }
    
    async def generate_followup_response(self, analysis: Dict, context: Dict) -> str:
        """Generate appropriate follow-up response"""
        if analysis['next_action'] == 'end_call':
            return "Thank you for your time. Have a wonderful day!"
        elif analysis['next_action'] == 'schedule_callback':
            return "I'd be happy to schedule a better time to chat. What works best for you this week?"
        elif analysis['next_action'] == 'continue':
            return analysis.get('suggested_response', "That's great to hear. Let me tell you more about how we can help...")
        else:
            return analysis.get('suggested_response', "Thank you for your interest. Let me connect you with a specialist.")

class CallingWorker:
    """Main calling worker implementation"""
    
    def __init__(self):
        self.redis = None
        self.db_pool = None
        self.twilio = TwilioClient(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        self.ai_handler = AIConversationHandler()
        self.running = False
        self.webhook_base_url = os.getenv('WEBHOOK_BASE_URL', 'https://api.flyfox.ai')
        
    async def initialize(self):
        """Initialize connections"""
        # Redis connection
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis = await aioredis.from_url(redis_url)
        
        # PostgreSQL connection pool
        db_url = os.getenv('DATABASE_URL')
        self.db_pool = await asyncpg.create_pool(db_url, min_size=5, max_size=20)
        
        logger.info("Calling worker initialized")
    
    async def initiate_call(self, contact: Dict, campaign: Dict) -> CallRecord:
        """Initiate an outbound call"""
        call_record = CallRecord(
            id=str(uuid.uuid4()),
            contact_id=contact['id'],
            campaign_id=campaign['id'],
            phone_number=contact['phone'],
            status=CallStatus.QUEUED
        )
        
        try:
            # Generate personalized script
            opening_script = await self.ai_handler.generate_opening_script(contact, campaign)
            
            # Create TwiML for the call
            twiml_url = f"{self.webhook_base_url}/webhooks/call/{call_record.id}/start"
            
            # Initiate call via Twilio
            call = self.twilio.calls.create(
                to=contact['phone'],
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=twiml_url,
                method='POST',
                record=True,
                recording_status_callback=f"{self.webhook_base_url}/webhooks/call/{call_record.id}/recording",
                status_callback=f"{self.webhook_base_url}/webhooks/call/{call_record.id}/status",
                timeout=30,
                machine_detection='Enable'
            )
            
            call_record.twilio_call_sid = call.sid
            call_record.status = CallStatus.INITIATED
            call_record.started_at = datetime.now(timezone.utc)
            
            # Store call record
            await self._save_call_record(call_record)
            
            # Store opening script in Redis for webhook access
            await self.redis.hset(
                f"call:{call_record.id}",
                mapping={
                    'opening_script': opening_script,
                    'contact': json.dumps(contact),
                    'campaign': json.dumps(campaign),
                    'stage': 'opening'
                }
            )
            
            logger.info(f"Call initiated: {call_record.id} to {contact['phone']}")
            return call_record
            
        except TwilioException as e:
            logger.error(f"Twilio error initiating call: {e}")
            call_record.status = CallStatus.FAILED
            call_record.outcome = CallOutcome.INVALID_NUMBER
            await self._save_call_record(call_record)
            raise
        except Exception as e:
            logger.error(f"Error initiating call: {e}")
            call_record.status = CallStatus.FAILED
            await self._save_call_record(call_record)
            raise
    
    async def handle_call_webhook(self, call_id: str, webhook_type: str, data: Dict) -> str:
        """Handle Twilio webhook callbacks"""
        try:
            if webhook_type == 'start':
                return await self._handle_call_start(call_id, data)
            elif webhook_type == 'gather':
                return await self._handle_call_gather(call_id, data)
            elif webhook_type == 'status':
                await self._handle_call_status(call_id, data)
                return ''
            elif webhook_type == 'recording':
                await self._handle_call_recording(call_id, data)
                return ''
            else:
                logger.warning(f"Unknown webhook type: {webhook_type}")
                return ''
                
        except Exception as e:
            logger.error(f"Error handling webhook {webhook_type} for call {call_id}: {e}")
            return self._generate_error_twiml()
    
    async def _handle_call_start(self, call_id: str, data: Dict) -> str:
        """Handle call start webhook"""
        # Get call context
        call_data = await self.redis.hgetall(f"call:{call_id}")
        
        if not call_data:
            logger.error(f"No call data found for {call_id}")
            return self._generate_error_twiml()
        
        # Check for answering machine
        if data.get('AnsweredBy') == 'machine_start':
            # Leave voicemail
            response = VoiceResponse()
            response.pause(length=2)
            response.say(
                "Hi, this is FlyFox AI. We have an exciting automation opportunity for your business. "
                "Please call us back at your convenience. Thank you!",
                voice='alice'
            )
            response.hangup()
            
            # Update call record
            await self._update_call_outcome(call_id, CallOutcome.VOICEMAIL)
            return str(response)
        
        # Human answered - start conversation
        opening_script = call_data.get('opening_script', 'Hello, this is FlyFox AI calling.')
        
        response = VoiceResponse()
        gather = Gather(
            input='speech',
            timeout=10,
            speech_timeout='auto',
            action=f"{self.webhook_base_url}/webhooks/call/{call_id}/gather",
            method='POST'
        )
        gather.say(opening_script, voice='alice')
        response.append(gather)
        
        # Fallback if no response
        response.say("I didn't hear a response. Thank you for your time. Goodbye!", voice='alice')
        response.hangup()
        
        return str(response)
    
    async def _handle_call_gather(self, call_id: str, data: Dict) -> str:
        """Handle speech input from call"""
        speech_result = data.get('SpeechResult', '').strip()
        
        if not speech_result:
            # No speech detected
            response = VoiceResponse()
            response.say("Thank you for your time. Have a great day!", voice='alice')
            response.hangup()
            return str(response)
        
        # Get call context
        call_data = await self.redis.hgetall(f"call:{call_id}")
        contact = json.loads(call_data.get('contact', '{}'))
        campaign = json.loads(call_data.get('campaign', '{}'))
        
        # Analyze response with AI
        context = {
            'purpose': campaign.get('purpose', 'Business outreach'),
            'stage': call_data.get('stage', 'opening'),
            'history': json.loads(call_data.get('history', '[]'))
        }
        
        analysis = await self.ai_handler.process_response(speech_result, context)
        
        # Update conversation history
        history = context['history']
        history.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'user_input': speech_result,
            'analysis': analysis
        })
        
        await self.redis.hset(
            f"call:{call_id}",
            'history', json.dumps(history)
        )
        
        # Generate response based on analysis
        response = VoiceResponse()
        
        if analysis['next_action'] == 'end_call':
            response.say(analysis['suggested_response'], voice='alice')
            response.hangup()
            await self._update_call_outcome(call_id, CallOutcome.NOT_INTERESTED, analysis)
        elif analysis['next_action'] == 'schedule_callback':
            response.say(analysis['suggested_response'], voice='alice')
            response.hangup()
            await self._update_call_outcome(call_id, CallOutcome.CALLBACK_REQUESTED, analysis)
        else:
            # Continue conversation
            gather = Gather(
                input='speech',
                timeout=10,
                speech_timeout='auto',
                action=f"{self.webhook_base_url}/webhooks/call/{call_id}/gather",
                method='POST'
            )
            gather.say(analysis['suggested_response'], voice='alice')
            response.append(gather)
            
            # Fallback
            response.say("Thank you for your time. We'll follow up soon!", voice='alice')
            response.hangup()
        
        return str(response)
    
    async def _handle_call_status(self, call_id: str, data: Dict):
        """Handle call status updates"""
        call_status = data.get('CallStatus')
        call_duration = data.get('CallDuration')
        
        # Update call record in database
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE call_records 
                SET status = $1, duration = $2, ended_at = $3
                WHERE id = $4
            """, call_status, call_duration, datetime.now(timezone.utc), call_id)
        
        logger.info(f"Call {call_id} status updated: {call_status}")
    
    async def _handle_call_recording(self, call_id: str, data: Dict):
        """Handle call recording webhook"""
        recording_url = data.get('RecordingUrl')
        
        if recording_url:
            # Update call record with recording URL
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE call_records 
                    SET recording_url = $1
                    WHERE id = $2
                """, recording_url, call_id)
            
            # Queue for transcription
            await self.redis.lpush('transcription_queue', json.dumps({
                'call_id': call_id,
                'recording_url': recording_url
            }))
            
            logger.info(f"Recording saved for call {call_id}: {recording_url}")
    
    async def _update_call_outcome(self, call_id: str, outcome: CallOutcome, analysis: Dict = None):
        """Update call outcome and analysis"""
        lead_score = analysis.get('lead_score', 5) if analysis else 5
        sentiment_score = self._sentiment_to_score(analysis.get('sentiment', 'neutral')) if analysis else 0.5
        
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE call_records 
                SET outcome = $1, lead_score = $2, sentiment_score = $3, ai_summary = $4
                WHERE id = $5
            """, outcome.value, lead_score, sentiment_score, 
                json.dumps(analysis) if analysis else None, call_id)
    
    def _sentiment_to_score(self, sentiment: str) -> float:
        """Convert sentiment to numeric score"""
        mapping = {
            'positive': 0.8,
            'neutral': 0.5,
            'negative': 0.2
        }
        return mapping.get(sentiment, 0.5)
    
    def _generate_error_twiml(self) -> str:
        """Generate error TwiML response"""
        response = VoiceResponse()
        response.say("We're experiencing technical difficulties. Please try again later.", voice='alice')
        response.hangup()
        return str(response)
    
    async def _save_call_record(self, call_record: CallRecord):
        """Save call record to database"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO call_records (
                    id, contact_id, campaign_id, phone_number, status, outcome,
                    duration, recording_url, transcript, ai_summary, sentiment_score,
                    lead_score, next_action, scheduled_callback, twilio_call_sid,
                    started_at, ended_at, created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)
            """, 
                call_record.id, call_record.contact_id, call_record.campaign_id,
                call_record.phone_number, call_record.status.value, 
                call_record.outcome.value if call_record.outcome else None,
                call_record.duration, call_record.recording_url, call_record.transcript,
                call_record.ai_summary, call_record.sentiment_score, call_record.lead_score,
                call_record.next_action, call_record.scheduled_callback,
                call_record.twilio_call_sid, call_record.started_at, call_record.ended_at,
                call_record.created_at
            )
    
    async def run(self):
        """Main worker loop"""
        self.running = True
        logger.info("Calling worker started")
        
        while self.running:
            try:
                # Listen for calling jobs
                job_data = await self.redis.brpop('calling_queue', timeout=5)
                
                if job_data:
                    queue_name, contact_json = job_data
                    contact = json.loads(contact_json)
                    
                    # Get campaign info
                    campaign_id = queue_name.decode().split(':')[1]
                    campaign_data = await self.redis.hgetall(f"campaign:{campaign_id}")
                    campaign = {k.decode(): v.decode() for k, v in campaign_data.items()}
                    
                    logger.info(f"Processing call for contact: {contact['id']}")
                    
                    # Check calling hours and compliance
                    if await self._can_call_now(contact):
                        await self.initiate_call(contact, campaign)
                    else:
                        # Reschedule for later
                        await self._reschedule_call(contact, campaign)
                    
            except Exception as e:
                logger.error(f"Error in calling worker: {e}")
                await asyncio.sleep(5)
    
    async def _can_call_now(self, contact: Dict) -> bool:
        """Check if we can call this contact now (compliance)"""
        # Check time zone and calling hours
        contact_tz = contact.get('timezone', 'America/New_York')
        # Implementation would check local time in contact's timezone
        # and ensure it's within acceptable calling hours (8 AM - 9 PM)
        
        # For now, simple check
        current_hour = datetime.now().hour
        return 8 <= current_hour <= 21
    
    async def _reschedule_call(self, contact: Dict, campaign: Dict):
        """Reschedule call for appropriate time"""
        # Calculate next appropriate calling time
        next_call_time = datetime.now() + timedelta(hours=1)
        
        # Add back to queue with delay
        await self.redis.zadd(
            'scheduled_calls',
            {json.dumps(contact): next_call_time.timestamp()}
        )
    
    async def stop(self):
        """Stop the worker"""
        self.running = False
        if self.redis:
            await self.redis.close()
        if self.db_pool:
            await self.db_pool.close()
        logger.info("Calling worker stopped")

async def main():
    """Main entry point"""
    worker = CallingWorker()
    
    try:
        await worker.initialize()
        await worker.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        await worker.stop()

if __name__ == "__main__":
    asyncio.run(main())