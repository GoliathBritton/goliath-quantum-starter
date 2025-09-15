#!/usr/bin/env python3
"""
Feedback Loop + Self-Evolution System
Every call → outcome data → NQBA retrains QUBO models
CRM pipeline → tracks every stage (lead → opportunity → closed deal)
Agents learn which phrasing works, which doesn't, and evolve hour by hour
"""

import asyncio
import json
import logging
import uuid
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import redis
import openai
from celery import Celery

# Import quantum components
try:
    from ..nqba.engine import NQBAEngine
    from .quantum_lead_scoring import QuantumLeadScorer
    from .ai_calling_agents import AICallingAgent
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.nqba.engine import NQBAEngine
    from src.agents.quantum_lead_scoring import QuantumLeadScorer
    from src.agents.ai_calling_agents import AICallingAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database models
Base = declarative_base()

class CallOutcome(Enum):
    ANSWERED = "answered"
    NO_ANSWER = "no_answer"
    VOICEMAIL = "voicemail"
    BUSY = "busy"
    INTERESTED = "interested"
    NOT_INTERESTED = "not_interested"
    CALLBACK_REQUESTED = "callback_requested"
    MEETING_SCHEDULED = "meeting_scheduled"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    HUNG_UP = "hung_up"
    WRONG_NUMBER = "wrong_number"

class LeadStage(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    OPPORTUNITY = "opportunity"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    NURTURE = "nurture"

class CallRecord(Base):
    """Detailed call tracking for learning"""
    __tablename__ = 'call_records'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, nullable=False)
    agent_id = Column(String, nullable=False)
    
    # Call details
    phone_number = Column(String, nullable=False)
    call_duration = Column(Integer, default=0)  # seconds
    outcome = Column(String, nullable=False)
    
    # Script and conversation
    script_version = Column(String)
    opening_line = Column(Text)
    conversation_transcript = Column(Text)
    objections_encountered = Column(JSON)
    responses_used = Column(JSON)
    
    # AI analysis
    sentiment_analysis = Column(JSON)
    engagement_metrics = Column(JSON)
    success_indicators = Column(JSON)
    
    # Quantum insights
    quantum_score_before = Column(Float)
    quantum_score_after = Column(Float)
    quantum_features = Column(JSON)
    
    # Performance metrics
    talk_time_ratio = Column(Float)  # agent vs prospect talk time
    interruption_count = Column(Integer, default=0)
    question_count = Column(Integer, default=0)
    objection_count = Column(Integer, default=0)
    
    # Timing
    called_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime)
    ended_at = Column(DateTime)
    
    # Follow-up
    next_action = Column(String)
    scheduled_callback = Column(DateTime)
    notes = Column(Text)
    
    # Cost tracking
    call_cost = Column(Float, default=0.0)
    ai_processing_cost = Column(Float, default=0.0)
    
class LeadJourney(Base):
    """Track complete lead lifecycle"""
    __tablename__ = 'lead_journeys'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, nullable=False, unique=True)
    
    # Current state
    current_stage = Column(String, default=LeadStage.NEW.value)
    current_score = Column(Float, default=0.0)
    priority_tier = Column(String, default="cold")
    
    # Journey tracking
    stage_history = Column(JSON, default=list)
    score_history = Column(JSON, default=list)
    touchpoint_history = Column(JSON, default=list)
    
    # Conversion metrics
    first_contact = Column(DateTime)
    last_contact = Column(DateTime)
    total_touchpoints = Column(Integer, default=0)
    total_call_time = Column(Integer, default=0)  # seconds
    
    # Outcomes
    conversion_probability = Column(Float, default=0.0)
    estimated_value = Column(Float, default=0.0)
    actual_value = Column(Float, default=0.0)
    
    # Learning data
    successful_patterns = Column(JSON, default=list)
    failed_patterns = Column(JSON, default=list)
    optimal_timing = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ScriptPerformance(Base):
    """Track script effectiveness"""
    __tablename__ = 'script_performance'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    script_id = Column(String, nullable=False)
    version = Column(String, nullable=False)
    
    # Script content
    opening_line = Column(Text)
    value_proposition = Column(Text)
    objection_responses = Column(JSON)
    closing_techniques = Column(JSON)
    
    # Performance metrics
    total_uses = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    average_call_duration = Column(Float, default=0.0)
    meeting_rate = Column(Float, default=0.0)
    
    # Detailed analytics
    outcome_distribution = Column(JSON, default=dict)
    industry_performance = Column(JSON, default=dict)
    time_of_day_performance = Column(JSON, default=dict)
    
    # A/B testing
    test_group = Column(String)
    control_group_performance = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@dataclass
class LearningInsight:
    """Structured learning insight from call data"""
    insight_type: str  # "script_optimization", "timing", "objection_handling", etc.
    confidence: float
    description: str
    data_points: int
    recommendation: str
    impact_estimate: float
    
class CallFeedback(BaseModel):
    call_id: str
    outcome: str
    duration: int
    transcript: str
    objections: List[str]
    sentiment_score: float
    next_action: str

class LearningUpdate(BaseModel):
    insights: List[Dict]
    model_updates: Dict
    performance_metrics: Dict

class FeedbackEvolutionEngine:
    """Main feedback and evolution system"""
    
    def __init__(self,
                 db_url: str = "postgresql://localhost/quantum_leads",
                 redis_url: str = "redis://localhost:6379",
                 openai_api_key: str = None):
        
        # Database
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        
        # Redis for real-time data
        self.redis_client = redis.from_url(redis_url)
        
        # AI client
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        
        # Quantum components
        self.nqba_engine = NQBAEngine()
        self.lead_scorer = QuantumLeadScorer(db_url, redis_url)
        
        # Learning models
        self.script_vectorizer = TfidfVectorizer(max_features=1000)
        self.outcome_predictor = None
        
        # Performance tracking
        self.learning_stats = {
            'total_calls_analyzed': 0,
            'insights_generated': 0,
            'model_updates': 0,
            'performance_improvements': 0,
            'last_learning_cycle': None
        }
        
        # Celery for background processing
        self.celery_app = Celery(
            'feedback_evolution',
            broker=redis_url,
            backend=redis_url
        )
        
        # Start background learning
        asyncio.create_task(self.continuous_learning_loop())
    
    async def record_call_outcome(self, call_feedback: CallFeedback) -> Dict:
        """Record call outcome and trigger learning"""
        
        session_db = self.SessionLocal()
        
        try:
            # Analyze conversation
            conversation_analysis = await self.analyze_conversation(
                call_feedback.transcript,
                call_feedback.outcome,
                call_feedback.objections
            )
            
            # Create call record
            call_record = CallRecord(
                id=call_feedback.call_id,
                lead_id=conversation_analysis.get('lead_id', 'unknown'),
                agent_id=conversation_analysis.get('agent_id', 'ai_agent_001'),
                call_duration=call_feedback.duration,
                outcome=call_feedback.outcome,
                conversation_transcript=call_feedback.transcript,
                objections_encountered=call_feedback.objections,
                sentiment_analysis={
                    'overall_sentiment': call_feedback.sentiment_score,
                    'sentiment_progression': conversation_analysis.get('sentiment_progression', []),
                    'emotional_peaks': conversation_analysis.get('emotional_peaks', [])
                },
                engagement_metrics=conversation_analysis.get('engagement_metrics', {}),
                success_indicators=conversation_analysis.get('success_indicators', {}),
                next_action=call_feedback.next_action
            )
            
            session_db.add(call_record)
            session_db.commit()
            
            # Update lead journey
            await self.update_lead_journey(call_feedback.call_id, call_feedback.outcome)
            
            # Trigger learning update
            self.celery_app.send_task('process_learning_update', args=[call_feedback.call_id])
            
            return {
                'status': 'recorded',
                'call_id': call_feedback.call_id,
                'learning_triggered': True,
                'analysis': conversation_analysis
            }
        
        finally:
            session_db.close()
    
    async def analyze_conversation(self, transcript: str, outcome: str, objections: List[str]) -> Dict:
        """Deep analysis of conversation for learning"""
        
        analysis_prompt = f"""
        Analyze this sales call conversation for learning insights:
        
        Transcript: {transcript[:2000]}...
        Outcome: {outcome}
        Objections: {objections}
        
        Provide detailed JSON analysis with:
        1. engagement_metrics: {
           "talk_time_ratio": float,
           "question_count": int,
           "interruption_count": int,
           "energy_level": 1-10
        }
        2. success_indicators: {
           "buying_signals": [list],
           "pain_points_identified": [list],
           "rapport_building": 1-10,
           "objection_handling_quality": 1-10
        }
        3. improvement_opportunities: [list of specific suggestions]
        4. script_effectiveness: {
           "opening_effectiveness": 1-10,
           "value_prop_clarity": 1-10,
           "closing_strength": 1-10
        }
        5. sentiment_progression: [list of sentiment scores throughout call]
        6. key_phrases: {
           "effective_phrases": [list],
           "ineffective_phrases": [list]
        }
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert sales conversation analyst."},
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        try:
            analysis = json.loads(response.choices[0].message.content)
        except:
            # Fallback analysis
            analysis = {
                "engagement_metrics": {"talk_time_ratio": 0.5, "question_count": 3, "interruption_count": 1, "energy_level": 5},
                "success_indicators": {"buying_signals": [], "pain_points_identified": [], "rapport_building": 5, "objection_handling_quality": 5},
                "improvement_opportunities": ["Improve opening engagement"],
                "script_effectiveness": {"opening_effectiveness": 5, "value_prop_clarity": 5, "closing_strength": 5},
                "sentiment_progression": [0.0, 0.1, 0.2],
                "key_phrases": {"effective_phrases": [], "ineffective_phrases": []}
            }
        
        return analysis
    
    async def update_lead_journey(self, call_id: str, outcome: str) -> None:
        """Update lead journey based on call outcome"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get call record
            call_record = session_db.query(CallRecord).filter(
                CallRecord.id == call_id
            ).first()
            
            if not call_record:
                return
            
            # Get or create lead journey
            journey = session_db.query(LeadJourney).filter(
                LeadJourney.lead_id == call_record.lead_id
            ).first()
            
            if not journey:
                journey = LeadJourney(
                    lead_id=call_record.lead_id,
                    first_contact=datetime.utcnow()
                )
                session_db.add(journey)
            
            # Update journey based on outcome
            new_stage = self.determine_new_stage(outcome, journey.current_stage)
            
            # Update stage history
            stage_history = journey.stage_history or []
            stage_history.append({
                'stage': new_stage,
                'timestamp': datetime.utcnow().isoformat(),
                'trigger': f"call_outcome_{outcome}"
            })
            
            # Update touchpoint history
            touchpoint_history = journey.touchpoint_history or []
            touchpoint_history.append({
                'type': 'phone_call',
                'outcome': outcome,
                'duration': call_record.call_duration,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Update journey
            journey.current_stage = new_stage
            journey.last_contact = datetime.utcnow()
            journey.total_touchpoints += 1
            journey.total_call_time += call_record.call_duration
            journey.stage_history = stage_history
            journey.touchpoint_history = touchpoint_history
            
            # Update conversion probability using quantum scoring
            quantum_insights = await self.lead_scorer.quantum_score_leads([{
                'lead_id': call_record.lead_id,
                'stage': new_stage,
                'touchpoints': journey.total_touchpoints,
                'last_outcome': outcome
            }])
            
            if quantum_insights:
                journey.conversion_probability = quantum_insights[0][1]
                journey.current_score = quantum_insights[0][1]
            
            session_db.commit()
        
        finally:
            session_db.close()
    
    def determine_new_stage(self, outcome: str, current_stage: str) -> str:
        """Determine new lead stage based on call outcome"""
        
        stage_transitions = {
            CallOutcome.INTERESTED.value: LeadStage.QUALIFIED.value,
            CallOutcome.MEETING_SCHEDULED.value: LeadStage.OPPORTUNITY.value,
            CallOutcome.QUALIFIED.value: LeadStage.OPPORTUNITY.value,
            CallOutcome.NOT_INTERESTED.value: LeadStage.CLOSED_LOST.value,
            CallOutcome.DISQUALIFIED.value: LeadStage.CLOSED_LOST.value,
            CallOutcome.CALLBACK_REQUESTED.value: LeadStage.NURTURE.value,
            CallOutcome.ANSWERED.value: LeadStage.CONTACTED.value,
            CallOutcome.VOICEMAIL.value: LeadStage.CONTACTED.value
        }
        
        return stage_transitions.get(outcome, current_stage)
    
    async def generate_learning_insights(self) -> List[LearningInsight]:
        """Generate actionable learning insights from call data"""
        
        session_db = self.SessionLocal()
        insights = []
        
        try:
            # Get recent call data
            recent_calls = session_db.query(CallRecord).filter(
                CallRecord.called_at >= datetime.utcnow() - timedelta(hours=24)
            ).all()
            
            if len(recent_calls) < 10:
                return insights
            
            # Analyze script performance
            script_insights = await self.analyze_script_performance(recent_calls)
            insights.extend(script_insights)
            
            # Analyze timing patterns
            timing_insights = await self.analyze_timing_patterns(recent_calls)
            insights.extend(timing_insights)
            
            # Analyze objection handling
            objection_insights = await self.analyze_objection_patterns(recent_calls)
            insights.extend(objection_insights)
            
            # Analyze conversion patterns
            conversion_insights = await self.analyze_conversion_patterns(recent_calls)
            insights.extend(conversion_insights)
            
            return insights
        
        finally:
            session_db.close()
    
    async def analyze_script_performance(self, calls: List[CallRecord]) -> List[LearningInsight]:
        """Analyze which scripts and phrases work best"""
        
        insights = []
        
        # Group calls by outcome
        successful_calls = [c for c in calls if c.outcome in [
            CallOutcome.INTERESTED.value,
            CallOutcome.MEETING_SCHEDULED.value,
            CallOutcome.QUALIFIED.value
        ]]
        
        unsuccessful_calls = [c for c in calls if c.outcome in [
            CallOutcome.NOT_INTERESTED.value,
            CallOutcome.HUNG_UP.value,
            CallOutcome.DISQUALIFIED.value
        ]]
        
        if len(successful_calls) >= 5 and len(unsuccessful_calls) >= 5:
            # Analyze opening lines
            successful_openings = [c.opening_line for c in successful_calls if c.opening_line]
            unsuccessful_openings = [c.opening_line for c in unsuccessful_calls if c.opening_line]
            
            if successful_openings and unsuccessful_openings:
                # Use AI to identify patterns
                pattern_analysis = await self.identify_phrase_patterns(
                    successful_openings, unsuccessful_openings, "opening_lines"
                )
                
                if pattern_analysis:
                    insights.append(LearningInsight(
                        insight_type="script_optimization",
                        confidence=0.8,
                        description=f"Opening line analysis: {pattern_analysis['insight']}",
                        data_points=len(successful_calls) + len(unsuccessful_calls),
                        recommendation=pattern_analysis['recommendation'],
                        impact_estimate=0.15  # 15% improvement estimate
                    ))
        
        return insights
    
    async def analyze_timing_patterns(self, calls: List[CallRecord]) -> List[LearningInsight]:
        """Analyze optimal calling times"""
        
        insights = []
        
        # Group by hour of day
        hourly_performance = {}
        
        for call in calls:
            hour = call.called_at.hour
            if hour not in hourly_performance:
                hourly_performance[hour] = {'total': 0, 'successful': 0}
            
            hourly_performance[hour]['total'] += 1
            if call.outcome in [CallOutcome.INTERESTED.value, CallOutcome.MEETING_SCHEDULED.value]:
                hourly_performance[hour]['successful'] += 1
        
        # Find best performing hours
        best_hours = []
        for hour, data in hourly_performance.items():
            if data['total'] >= 5:  # Minimum sample size
                success_rate = data['successful'] / data['total']
                if success_rate > 0.2:  # 20% success rate threshold
                    best_hours.append((hour, success_rate))
        
        if best_hours:
            best_hours.sort(key=lambda x: x[1], reverse=True)
            top_hour = best_hours[0]
            
            insights.append(LearningInsight(
                insight_type="timing_optimization",
                confidence=0.7,
                description=f"Hour {top_hour[0]}:00 shows {top_hour[1]:.1%} success rate",
                data_points=sum(data['total'] for data in hourly_performance.values()),
                recommendation=f"Increase call volume during {top_hour[0]}:00-{top_hour[0]+1}:00",
                impact_estimate=0.1
            ))
        
        return insights
    
    async def analyze_objection_patterns(self, calls: List[CallRecord]) -> List[LearningInsight]:
        """Analyze objection handling effectiveness"""
        
        insights = []
        
        # Collect objection data
        objection_outcomes = {}
        
        for call in calls:
            if call.objections_encountered:
                for objection in call.objections_encountered:
                    if objection not in objection_outcomes:
                        objection_outcomes[objection] = {'total': 0, 'overcome': 0}
                    
                    objection_outcomes[objection]['total'] += 1
                    if call.outcome in [CallOutcome.INTERESTED.value, CallOutcome.MEETING_SCHEDULED.value]:
                        objection_outcomes[objection]['overcome'] += 1
        
        # Find problematic objections
        for objection, data in objection_outcomes.items():
            if data['total'] >= 3:  # Minimum occurrences
                overcome_rate = data['overcome'] / data['total']
                if overcome_rate < 0.3:  # Low success rate
                    insights.append(LearningInsight(
                        insight_type="objection_handling",
                        confidence=0.8,
                        description=f"Objection '{objection}' has low overcome rate: {overcome_rate:.1%}",
                        data_points=data['total'],
                        recommendation=f"Develop better responses for '{objection}' objection",
                        impact_estimate=0.12
                    ))
        
        return insights
    
    async def analyze_conversion_patterns(self, calls: List[CallRecord]) -> List[LearningInsight]:
        """Analyze what leads to conversions"""
        
        insights = []
        
        # Analyze call duration vs outcome
        successful_durations = []
        unsuccessful_durations = []
        
        for call in calls:
            if call.outcome in [CallOutcome.INTERESTED.value, CallOutcome.MEETING_SCHEDULED.value]:
                successful_durations.append(call.call_duration)
            elif call.outcome in [CallOutcome.NOT_INTERESTED.value, CallOutcome.HUNG_UP.value]:
                unsuccessful_durations.append(call.call_duration)
        
        if len(successful_durations) >= 5 and len(unsuccessful_durations) >= 5:
            avg_successful = np.mean(successful_durations)
            avg_unsuccessful = np.mean(unsuccessful_durations)
            
            if avg_successful > avg_unsuccessful * 1.5:  # Significant difference
                insights.append(LearningInsight(
                    insight_type="conversion_pattern",
                    confidence=0.7,
                    description=f"Successful calls average {avg_successful:.0f}s vs {avg_unsuccessful:.0f}s for unsuccessful",
                    data_points=len(successful_durations) + len(unsuccessful_durations),
                    recommendation="Focus on extending conversation time with engaged prospects",
                    impact_estimate=0.08
                ))
        
        return insights
    
    async def identify_phrase_patterns(self, successful_phrases: List[str], unsuccessful_phrases: List[str], context: str) -> Dict:
        """Use AI to identify effective vs ineffective phrase patterns"""
        
        analysis_prompt = f"""
        Analyze these {context} for sales effectiveness patterns:
        
        SUCCESSFUL {context.upper()}:
        {chr(10).join(successful_phrases[:10])}
        
        UNSUCCESSFUL {context.upper()}:
        {chr(10).join(unsuccessful_phrases[:10])}
        
        Identify:
        1. Common patterns in successful examples
        2. Common patterns in unsuccessful examples
        3. Key differences
        4. Specific recommendation for improvement
        
        Return JSON with:
        {
          "successful_patterns": [list],
          "unsuccessful_patterns": [list],
          "key_differences": [list],
          "insight": "brief insight",
          "recommendation": "specific actionable recommendation"
        }
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert sales language analyst."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return json.loads(response.choices[0].message.content)
        except:
            return None
    
    async def update_quantum_models(self, insights: List[LearningInsight]) -> Dict:
        """Update QUBO models based on learning insights"""
        
        model_updates = {
            'script_weights': {},
            'timing_weights': {},
            'objection_weights': {},
            'feature_importance': {}
        }
        
        for insight in insights:
            if insight.insight_type == "script_optimization":
                # Update script effectiveness weights
                model_updates['script_weights'][insight.description] = insight.impact_estimate
            
            elif insight.insight_type == "timing_optimization":
                # Update timing preference weights
                model_updates['timing_weights'][insight.description] = insight.impact_estimate
            
            elif insight.insight_type == "objection_handling":
                # Update objection difficulty weights
                model_updates['objection_weights'][insight.description] = insight.impact_estimate
        
        # Apply updates to NQBA engine
        try:
            await self.nqba_engine.update_model_weights(model_updates)
            
            # Update lead scorer
            await self.lead_scorer.retrain_with_feedback(insights)
            
            return {
                'status': 'updated',
                'models_updated': len(model_updates),
                'insights_applied': len(insights)
            }
        except Exception as e:
            logger.error(f"Error updating quantum models: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def continuous_learning_loop(self):
        """Continuous learning background process"""
        
        while True:
            try:
                # Generate insights every hour
                insights = await self.generate_learning_insights()
                
                if insights:
                    # Update models
                    update_result = await self.update_quantum_models(insights)
                    
                    # Update stats
                    self.learning_stats['insights_generated'] += len(insights)
                    self.learning_stats['model_updates'] += 1
                    self.learning_stats['last_learning_cycle'] = datetime.utcnow().isoformat()
                    
                    logger.info(f"Learning cycle completed: {len(insights)} insights, {update_result}")
                
                # Wait 1 hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in learning loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def get_learning_stats(self) -> Dict:
        """Get learning system statistics"""
        session_db = self.SessionLocal()
        
        try:
            total_calls = session_db.query(CallRecord).count()
            recent_calls = session_db.query(CallRecord).filter(
                CallRecord.called_at >= datetime.utcnow() - timedelta(hours=24)
            ).count()
            
            self.learning_stats.update({
                'total_calls_analyzed': total_calls,
                'recent_calls_24h': recent_calls
            })
            
            return self.learning_stats
        
        finally:
            session_db.close()

# FastAPI application
app = FastAPI(
    title="Quantum Feedback Evolution",
    description="Self-evolving AI system that learns from every call",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global feedback engine
feedback_engine = None

@app.on_event("startup")
async def startup_event():
    global feedback_engine
    
    import os
    feedback_engine = FeedbackEvolutionEngine(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    logger.info("Quantum Feedback Evolution system started")

@app.post("/feedback/call")
async def record_call_feedback(call_feedback: CallFeedback):
    """Record call outcome and trigger learning"""
    try:
        result = await feedback_engine.record_call_outcome(call_feedback)
        return result
    except Exception as e:
        logger.error(f"Error recording call feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights/generate")
async def generate_insights():
    """Generate learning insights from recent data"""
    try:
        insights = await feedback_engine.generate_learning_insights()
        return {
            'insights': [asdict(insight) for insight in insights],
            'count': len(insights)
        }
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/models/update")
async def update_models():
    """Manually trigger model updates"""
    try:
        insights = await feedback_engine.generate_learning_insights()
        result = await feedback_engine.update_quantum_models(insights)
        return result
    except Exception as e:
        logger.error(f"Error updating models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_learning_stats():
    """Get learning system statistics"""
    return feedback_engine.get_learning_stats()

@app.get("/journey/{lead_id}")
async def get_lead_journey(lead_id: str):
    """Get complete lead journey"""
    session_db = feedback_engine.SessionLocal()
    
    try:
        journey = session_db.query(LeadJourney).filter(
            LeadJourney.lead_id == lead_id
        ).first()
        
        if not journey:
            raise HTTPException(status_code=404, detail="Lead journey not found")
        
        # Get call history
        calls = session_db.query(CallRecord).filter(
            CallRecord.lead_id == lead_id
        ).order_by(CallRecord.called_at.desc()).all()
        
        return {
            'journey': {
                'lead_id': journey.lead_id,
                'current_stage': journey.current_stage,
                'current_score': journey.current_score,
                'conversion_probability': journey.conversion_probability,
                'total_touchpoints': journey.total_touchpoints,
                'stage_history': journey.stage_history,
                'touchpoint_history': journey.touchpoint_history
            },
            'calls': [{
                'id': call.id,
                'outcome': call.outcome,
                'duration': call.call_duration,
                'called_at': call.called_at.isoformat(),
                'sentiment_score': call.sentiment_analysis.get('overall_sentiment', 0) if call.sentiment_analysis else 0
            } for call in calls]
        }
    
    finally:
        session_db.close()

if __name__ == "__main__":
    uvicorn.run(
        "feedback_evolution:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    )