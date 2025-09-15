#!/usr/bin/env python3
"""
Dynamic Playbook Generator
Built on qdLLM + QNLP
Generates real-time scripts per persona, per industry, per objection path
Self-updates daily based on previous day's calls
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
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import openai
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

# Import quantum components
try:
    from ..nqba.engine import NQBAEngine
    from ..quantum.qnlp_processor import QNLPProcessor
    from .feedback_evolution import FeedbackEvolutionEngine
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.nqba.engine import NQBAEngine
    from src.quantum.qnlp_processor import QNLPProcessor
    from src.agents.feedback_evolution import FeedbackEvolutionEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database models
Base = declarative_base()

class PlaybookType(Enum):
    COLD_OUTREACH = "cold_outreach"
    WARM_FOLLOW_UP = "warm_follow_up"
    DEMO_PRESENTATION = "demo_presentation"
    OBJECTION_HANDLING = "objection_handling"
    CLOSING_SEQUENCE = "closing_sequence"
    NURTURE_SEQUENCE = "nurture_sequence"

class IndustryVertical(Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    EDUCATION = "education"
    REAL_ESTATE = "real_estate"
    PROFESSIONAL_SERVICES = "professional_services"

class PersonaType(Enum):
    C_LEVEL = "c_level"
    VP_DIRECTOR = "vp_director"
    MANAGER = "manager"
    INDIVIDUAL_CONTRIBUTOR = "individual_contributor"
    TECHNICAL_DECISION_MAKER = "technical_decision_maker"
    FINANCIAL_DECISION_MAKER = "financial_decision_maker"

class PlaybookTemplate(Base):
    """Dynamic playbook templates"""
    __tablename__ = 'playbook_templates'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    playbook_type = Column(String, nullable=False)
    
    # Targeting
    industry_vertical = Column(String)
    persona_type = Column(String)
    company_size = Column(String)  # "startup", "smb", "mid_market", "enterprise"
    
    # Content structure
    template_structure = Column(JSON)  # Sections and flow
    variable_placeholders = Column(JSON)  # Dynamic content slots
    quantum_features = Column(JSON)  # QNLP-derived features
    
    # Performance data
    usage_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    average_engagement = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    
    # Learning data
    effective_phrases = Column(JSON, default=list)
    ineffective_phrases = Column(JSON, default=list)
    optimal_timing = Column(JSON)
    objection_patterns = Column(JSON, default=list)
    
    # Versioning
    version = Column(String, default="1.0")
    parent_template_id = Column(String)  # For A/B testing
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_optimized = Column(DateTime)

class GeneratedPlaybook(Base):
    """Generated playbook instances"""
    __tablename__ = 'generated_playbooks'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String, nullable=False)
    
    # Target context
    lead_id = Column(String)
    company_name = Column(String)
    contact_name = Column(String)
    industry = Column(String)
    persona = Column(String)
    
    # Generated content
    full_script = Column(Text)
    sections = Column(JSON)  # Structured sections
    personalization_data = Column(JSON)
    quantum_insights = Column(JSON)
    
    # Performance tracking
    times_used = Column(Integer, default=0)
    outcomes = Column(JSON, default=list)
    effectiveness_score = Column(Float, default=0.0)
    
    # Metadata
    generation_model = Column(String, default="qdLLM-v1")
    generation_timestamp = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # For cache management

@dataclass
class PlaybookRequest:
    """Request for playbook generation"""
    playbook_type: str
    industry: str
    persona: str
    company_name: str
    contact_name: str
    company_size: str
    specific_context: Optional[Dict] = None
    urgency_level: str = "medium"
    
class PlaybookGenerationRequest(BaseModel):
    playbook_type: str
    industry: str
    persona: str
    company_name: str
    contact_name: str
    company_size: str = "smb"
    specific_context: Optional[Dict] = None
    urgency_level: str = "medium"

class PlaybookResponse(BaseModel):
    playbook_id: str
    script_sections: Dict
    personalization_notes: List[str]
    quantum_insights: Dict
    estimated_effectiveness: float

class QDLLMEngine:
    """Quantum-enhanced Large Language Model for playbook generation"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.AsyncOpenAI(api_key=openai_api_key)
        self.qnlp_processor = QNLPProcessor()
        
        # Load quantum-enhanced models
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModel.from_pretrained("microsoft/DialoGPT-medium")
        
        # Quantum feature extractors
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.topic_modeler = LatentDirichletAllocation(n_components=10, random_state=42)
        
        # Performance cache
        self.phrase_effectiveness_cache = {}
        
    async def generate_quantum_enhanced_script(self, 
                                             request: PlaybookRequest,
                                             template: PlaybookTemplate,
                                             historical_data: List[Dict]) -> Dict:
        """Generate script using quantum-enhanced language processing"""
        
        # Extract quantum features from context
        quantum_features = await self.qnlp_processor.extract_quantum_features({
            'industry': request.industry,
            'persona': request.persona,
            'company_context': request.specific_context or {},
            'historical_performance': historical_data
        })
        
        # Build context-aware prompt
        context_prompt = self.build_context_prompt(request, template, quantum_features)
        
        # Generate base script using GPT-4
        base_script = await self.generate_base_script(context_prompt)
        
        # Enhance with quantum insights
        enhanced_script = await self.apply_quantum_enhancements(
            base_script, quantum_features, historical_data
        )
        
        # Optimize phrases based on historical performance
        optimized_script = await self.optimize_phrase_selection(
            enhanced_script, template.effective_phrases, template.ineffective_phrases
        )
        
        return {
            'script_sections': optimized_script,
            'quantum_features': quantum_features,
            'optimization_applied': True,
            'confidence_score': quantum_features.get('confidence', 0.8)
        }
    
    def build_context_prompt(self, request: PlaybookRequest, template: PlaybookTemplate, quantum_features: Dict) -> str:
        """Build comprehensive context prompt for script generation"""
        
        prompt = f"""
        Generate a high-converting {request.playbook_type} script for:
        
        TARGET CONTEXT:
        - Company: {request.company_name}
        - Contact: {request.contact_name}
        - Industry: {request.industry}
        - Persona: {request.persona}
        - Company Size: {request.company_size}
        - Urgency: {request.urgency_level}
        
        QUANTUM INSIGHTS:
        - Optimal Communication Style: {quantum_features.get('communication_style', 'professional')}
        - Key Pain Points: {quantum_features.get('pain_points', [])}
        - Decision Factors: {quantum_features.get('decision_factors', [])}
        - Engagement Patterns: {quantum_features.get('engagement_patterns', {})}
        
        TEMPLATE STRUCTURE:
        {json.dumps(template.template_structure, indent=2)}
        
        PROVEN EFFECTIVE PHRASES:
        {template.effective_phrases[:10] if template.effective_phrases else []}
        
        AVOID THESE PHRASES:
        {template.ineffective_phrases[:5] if template.ineffective_phrases else []}
        
        Generate a script that:
        1. Follows the template structure exactly
        2. Incorporates quantum insights naturally
        3. Uses proven effective phrases where appropriate
        4. Avoids ineffective patterns
        5. Personalizes for the specific target
        6. Optimizes for {request.urgency_level} urgency
        
        Return as JSON with sections matching the template structure.
        """
        
        return prompt
    
    async def generate_base_script(self, context_prompt: str) -> Dict:
        """Generate base script using GPT-4"""
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert sales script writer with deep knowledge of psychology, persuasion, and industry-specific communication patterns."
                },
                {
                    "role": "user",
                    "content": context_prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        try:
            script_content = response.choices[0].message.content.strip()
            # Try to parse as JSON, fallback to structured text
            if script_content.startswith('{'):
                return json.loads(script_content)
            else:
                # Parse structured text into sections
                return self.parse_structured_script(script_content)
        except Exception as e:
            logger.error(f"Error parsing script: {e}")
            return self.create_fallback_script()
    
    async def apply_quantum_enhancements(self, base_script: Dict, quantum_features: Dict, historical_data: List[Dict]) -> Dict:
        """Apply quantum-derived enhancements to the script"""
        
        enhanced_script = base_script.copy()
        
        # Apply quantum communication style adjustments
        communication_style = quantum_features.get('communication_style', 'professional')
        
        for section_name, content in enhanced_script.items():
            if isinstance(content, str):
                # Adjust tone based on quantum insights
                enhanced_content = await self.adjust_communication_style(
                    content, communication_style, quantum_features
                )
                enhanced_script[section_name] = enhanced_content
        
        # Add quantum-derived objection handling
        if 'objection_responses' not in enhanced_script:
            enhanced_script['objection_responses'] = await self.generate_quantum_objection_responses(
                quantum_features, historical_data
            )
        
        # Add quantum timing cues
        enhanced_script['timing_cues'] = quantum_features.get('optimal_timing', {})
        
        return enhanced_script
    
    async def adjust_communication_style(self, content: str, style: str, quantum_features: Dict) -> str:
        """Adjust content based on quantum-derived communication style"""
        
        style_adjustments = {
            'analytical': {
                'add_phrases': ['data shows', 'research indicates', 'metrics demonstrate'],
                'tone': 'logical and fact-based'
            },
            'relationship_focused': {
                'add_phrases': ['I understand', 'many of our clients', 'partnership'],
                'tone': 'warm and collaborative'
            },
            'results_oriented': {
                'add_phrases': ['bottom line', 'ROI', 'measurable impact'],
                'tone': 'direct and outcome-focused'
            },
            'innovative': {
                'add_phrases': ['cutting-edge', 'breakthrough', 'next-generation'],
                'tone': 'forward-thinking and exciting'
            }
        }
        
        if style in style_adjustments:
            adjustment = style_adjustments[style]
            
            # Use AI to naturally incorporate style elements
            style_prompt = f"""
            Adjust this sales script content to be more {adjustment['tone']}:
            
            Original: {content}
            
            Incorporate these concepts naturally: {adjustment['add_phrases']}
            
            Keep the core message but adjust the style and phrasing.
            Return only the adjusted content.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at adjusting communication styles."},
                    {"role": "user", "content": style_prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        
        return content
    
    async def generate_quantum_objection_responses(self, quantum_features: Dict, historical_data: List[Dict]) -> Dict:
        """Generate objection responses based on quantum insights"""
        
        common_objections = [
            "too expensive",
            "not the right time",
            "need to think about it",
            "happy with current solution",
            "not interested",
            "send me information"
        ]
        
        objection_responses = {}
        
        for objection in common_objections:
            # Find successful responses from historical data
            successful_responses = []
            for record in historical_data:
                if record.get('objection') == objection and record.get('outcome') == 'overcome':
                    successful_responses.append(record.get('response', ''))
            
            # Generate quantum-enhanced response
            response_prompt = f"""
            Generate a response to the objection: "{objection}"
            
            Context:
            - Communication style: {quantum_features.get('communication_style', 'professional')}
            - Key pain points: {quantum_features.get('pain_points', [])}
            - Decision factors: {quantum_features.get('decision_factors', [])}
            
            Successful responses from history:
            {successful_responses[:3] if successful_responses else ['No historical data']}
            
            Create a response that:
            1. Acknowledges the objection
            2. Addresses the underlying concern
            3. Redirects to value
            4. Asks for next step
            
            Keep it under 100 words.
            """
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at handling sales objections."},
                    {"role": "user", "content": response_prompt}
                ],
                max_tokens=200,
                temperature=0.6
            )
            
            objection_responses[objection] = response.choices[0].message.content.strip()
        
        return objection_responses
    
    async def optimize_phrase_selection(self, script: Dict, effective_phrases: List[str], ineffective_phrases: List[str]) -> Dict:
        """Optimize phrase selection based on historical performance"""
        
        optimized_script = {}
        
        for section_name, content in script.items():
            if isinstance(content, str):
                optimized_content = content
                
                # Replace ineffective phrases with effective ones
                for ineffective in ineffective_phrases:
                    if ineffective.lower() in optimized_content.lower():
                        # Find similar effective phrase
                        replacement = self.find_similar_effective_phrase(ineffective, effective_phrases)
                        if replacement:
                            optimized_content = optimized_content.replace(ineffective, replacement)
                
                optimized_script[section_name] = optimized_content
            else:
                optimized_script[section_name] = content
        
        return optimized_script
    
    def find_similar_effective_phrase(self, ineffective_phrase: str, effective_phrases: List[str]) -> Optional[str]:
        """Find effective phrase similar to ineffective one"""
        
        if not effective_phrases:
            return None
        
        # Simple similarity matching (could be enhanced with embeddings)
        ineffective_words = set(ineffective_phrase.lower().split())
        
        best_match = None
        best_score = 0
        
        for effective_phrase in effective_phrases:
            effective_words = set(effective_phrase.lower().split())
            overlap = len(ineffective_words.intersection(effective_words))
            score = overlap / len(ineffective_words.union(effective_words))
            
            if score > best_score:
                best_score = score
                best_match = effective_phrase
        
        return best_match if best_score > 0.3 else None
    
    def parse_structured_script(self, script_text: str) -> Dict:
        """Parse structured text into script sections"""
        
        sections = {}
        current_section = "opening"
        current_content = []
        
        lines = script_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            if any(keyword in line.lower() for keyword in ['opening:', 'introduction:', 'value prop', 'demo:', 'closing:', 'objection']):
                # Save previous section
                if current_content:
                    sections[current_section] = ' '.join(current_content)
                
                # Start new section
                current_section = line.lower().replace(':', '').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = ' '.join(current_content)
        
        return sections
    
    def create_fallback_script(self) -> Dict:
        """Create fallback script structure"""
        
        return {
            "opening": "Hi [Name], this is [Agent] from [Company]. I hope I'm catching you at a good time?",
            "value_proposition": "I'm reaching out because we help companies like [Company] achieve [specific benefit].",
            "discovery": "Can I ask you a quick question about [relevant pain point]?",
            "presentation": "Based on what you've shared, here's how we can help...",
            "closing": "Does this sound like something worth exploring further?"
        }

class DynamicPlaybookGenerator:
    """Main playbook generation system"""
    
    def __init__(self,
                 openai_api_key: str,
                 db_url: str = "postgresql://localhost/quantum_leads",
                 redis_url: str = "redis://localhost:6379"):
        
        # Database
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        
        # Redis for caching
        self.redis_client = redis.from_url(redis_url)
        
        # Quantum components
        self.nqba_engine = NQBAEngine()
        self.qdllm_engine = QDLLMEngine(openai_api_key)
        
        # Feedback system
        self.feedback_engine = FeedbackEvolutionEngine(db_url, redis_url, openai_api_key)
        
        # Performance tracking
        self.generation_stats = {
            'total_playbooks_generated': 0,
            'templates_optimized': 0,
            'daily_updates_performed': 0,
            'average_effectiveness': 0.0
        }
        
        # Initialize default templates
        asyncio.create_task(self.initialize_default_templates())
        
        # Start daily optimization
        asyncio.create_task(self.daily_optimization_loop())
    
    async def generate_playbook(self, request: PlaybookGenerationRequest) -> PlaybookResponse:
        """Generate personalized playbook"""
        
        session_db = self.SessionLocal()
        
        try:
            # Find best matching template
            template = await self.find_best_template(
                request.playbook_type,
                request.industry,
                request.persona,
                request.company_size
            )
            
            if not template:
                # Create new template
                template = await self.create_new_template(
                    request.playbook_type,
                    request.industry,
                    request.persona,
                    request.company_size
                )
            
            # Get historical performance data
            historical_data = await self.get_historical_performance_data(
                request.industry, request.persona
            )
            
            # Generate quantum-enhanced script
            playbook_request = PlaybookRequest(
                playbook_type=request.playbook_type,
                industry=request.industry,
                persona=request.persona,
                company_name=request.company_name,
                contact_name=request.contact_name,
                company_size=request.company_size,
                specific_context=request.specific_context,
                urgency_level=request.urgency_level
            )
            
            generated_content = await self.qdllm_engine.generate_quantum_enhanced_script(
                playbook_request, template, historical_data
            )
            
            # Create playbook record
            playbook_id = str(uuid.uuid4())
            
            generated_playbook = GeneratedPlaybook(
                id=playbook_id,
                template_id=template.id,
                lead_id=request.specific_context.get('lead_id') if request.specific_context else None,
                company_name=request.company_name,
                contact_name=request.contact_name,
                industry=request.industry,
                persona=request.persona,
                full_script=json.dumps(generated_content['script_sections']),
                sections=generated_content['script_sections'],
                quantum_insights=generated_content['quantum_features'],
                effectiveness_score=generated_content['confidence_score'],
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            
            session_db.add(generated_playbook)
            session_db.commit()
            
            # Update stats
            self.generation_stats['total_playbooks_generated'] += 1
            
            # Generate personalization notes
            personalization_notes = await self.generate_personalization_notes(
                generated_content, request
            )
            
            return PlaybookResponse(
                playbook_id=playbook_id,
                script_sections=generated_content['script_sections'],
                personalization_notes=personalization_notes,
                quantum_insights=generated_content['quantum_features'],
                estimated_effectiveness=generated_content['confidence_score']
            )
        
        finally:
            session_db.close()
    
    async def find_best_template(self, playbook_type: str, industry: str, persona: str, company_size: str) -> Optional[PlaybookTemplate]:
        """Find best matching template"""
        
        session_db = self.SessionLocal()
        
        try:
            # Exact match first
            template = session_db.query(PlaybookTemplate).filter(
                PlaybookTemplate.playbook_type == playbook_type,
                PlaybookTemplate.industry_vertical == industry,
                PlaybookTemplate.persona_type == persona,
                PlaybookTemplate.company_size == company_size
            ).order_by(PlaybookTemplate.success_rate.desc()).first()
            
            if template:
                return template
            
            # Partial match - same type and industry
            template = session_db.query(PlaybookTemplate).filter(
                PlaybookTemplate.playbook_type == playbook_type,
                PlaybookTemplate.industry_vertical == industry
            ).order_by(PlaybookTemplate.success_rate.desc()).first()
            
            if template:
                return template
            
            # Generic match - same type only
            template = session_db.query(PlaybookTemplate).filter(
                PlaybookTemplate.playbook_type == playbook_type
            ).order_by(PlaybookTemplate.success_rate.desc()).first()
            
            return template
        
        finally:
            session_db.close()
    
    async def create_new_template(self, playbook_type: str, industry: str, persona: str, company_size: str) -> PlaybookTemplate:
        """Create new template for specific context"""
        
        session_db = self.SessionLocal()
        
        try:
            # Define template structure based on type
            template_structures = {
                PlaybookType.COLD_OUTREACH.value: {
                    "opening": "Initial greeting and introduction",
                    "pattern_interrupt": "Attention-grabbing statement",
                    "value_proposition": "Clear value statement",
                    "discovery_question": "Qualifying question",
                    "social_proof": "Credibility statement",
                    "call_to_action": "Next step request"
                },
                PlaybookType.DEMO_PRESENTATION.value: {
                    "agenda_setting": "Meeting agenda and expectations",
                    "discovery": "Needs assessment questions",
                    "demo_flow": "Product demonstration sequence",
                    "benefit_reinforcement": "Value reinforcement",
                    "objection_handling": "Address concerns",
                    "next_steps": "Clear follow-up actions"
                },
                PlaybookType.OBJECTION_HANDLING.value: {
                    "acknowledge": "Acknowledge the objection",
                    "clarify": "Understand the real concern",
                    "respond": "Address with value",
                    "confirm": "Ensure resolution",
                    "advance": "Move forward"
                }
            }
            
            structure = template_structures.get(
                playbook_type,
                template_structures[PlaybookType.COLD_OUTREACH.value]
            )
            
            template = PlaybookTemplate(
                name=f"{playbook_type}_{industry}_{persona}_{company_size}",
                playbook_type=playbook_type,
                industry_vertical=industry,
                persona_type=persona,
                company_size=company_size,
                template_structure=structure,
                variable_placeholders={
                    "company_name": "[Company]",
                    "contact_name": "[Name]",
                    "agent_name": "[Agent]",
                    "specific_benefit": "[Benefit]",
                    "pain_point": "[Pain Point]"
                }
            )
            
            session_db.add(template)
            session_db.commit()
            
            return template
        
        finally:
            session_db.close()
    
    async def get_historical_performance_data(self, industry: str, persona: str) -> List[Dict]:
        """Get historical performance data for context"""
        
        # Get data from feedback engine
        try:
            insights = await self.feedback_engine.generate_learning_insights()
            
            # Filter for relevant industry/persona
            relevant_data = []
            for insight in insights:
                if industry.lower() in insight.description.lower() or persona.lower() in insight.description.lower():
                    relevant_data.append({
                        'type': insight.insight_type,
                        'description': insight.description,
                        'recommendation': insight.recommendation,
                        'confidence': insight.confidence,
                        'impact': insight.impact_estimate
                    })
            
            return relevant_data
        except:
            return []
    
    async def generate_personalization_notes(self, generated_content: Dict, request: PlaybookGenerationRequest) -> List[str]:
        """Generate personalization notes for the agent"""
        
        notes = []
        
        # Add quantum insights as notes
        quantum_features = generated_content.get('quantum_features', {})
        
        if quantum_features.get('communication_style'):
            notes.append(f"Use {quantum_features['communication_style']} communication style")
        
        if quantum_features.get('pain_points'):
            notes.append(f"Focus on these pain points: {', '.join(quantum_features['pain_points'][:3])}")
        
        if quantum_features.get('optimal_timing'):
            timing = quantum_features['optimal_timing']
            if isinstance(timing, dict) and 'best_time' in timing:
                notes.append(f"Best calling time: {timing['best_time']}")
        
        # Add context-specific notes
        if request.urgency_level == "high":
            notes.append("High urgency - be direct and focus on immediate value")
        elif request.urgency_level == "low":
            notes.append("Low urgency - build relationship and educate")
        
        # Add industry-specific notes
        industry_notes = {
            "technology": "Focus on innovation and competitive advantage",
            "healthcare": "Emphasize compliance and patient outcomes",
            "finance": "Highlight ROI and risk mitigation",
            "manufacturing": "Focus on efficiency and cost reduction"
        }
        
        if request.industry in industry_notes:
            notes.append(industry_notes[request.industry])
        
        return notes
    
    async def daily_optimization_loop(self):
        """Daily template optimization based on performance"""
        
        while True:
            try:
                # Wait until next optimization time (daily at 2 AM)
                now = datetime.utcnow()
                next_optimization = now.replace(hour=2, minute=0, second=0, microsecond=0)
                if next_optimization <= now:
                    next_optimization += timedelta(days=1)
                
                wait_seconds = (next_optimization - now).total_seconds()
                await asyncio.sleep(wait_seconds)
                
                # Perform optimization
                await self.optimize_templates_daily()
                
                self.generation_stats['daily_updates_performed'] += 1
                logger.info("Daily template optimization completed")
                
            except Exception as e:
                logger.error(f"Error in daily optimization: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def optimize_templates_daily(self):
        """Optimize templates based on previous day's performance"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get yesterday's performance data
            yesterday = datetime.utcnow() - timedelta(days=1)
            
            # Get all templates that were used yesterday
            used_templates = session_db.query(PlaybookTemplate).join(
                GeneratedPlaybook,
                PlaybookTemplate.id == GeneratedPlaybook.template_id
            ).filter(
                GeneratedPlaybook.generation_timestamp >= yesterday
            ).distinct().all()
            
            for template in used_templates:
                await self.optimize_single_template(template)
            
            session_db.commit()
            
        finally:
            session_db.close()
    
    async def optimize_single_template(self, template: PlaybookTemplate):
        """Optimize a single template based on performance data"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get recent playbooks using this template
            recent_playbooks = session_db.query(GeneratedPlaybook).filter(
                GeneratedPlaybook.template_id == template.id,
                GeneratedPlaybook.generation_timestamp >= datetime.utcnow() - timedelta(days=7)
            ).all()
            
            if len(recent_playbooks) < 5:  # Need minimum data
                return
            
            # Calculate performance metrics
            total_uses = len(recent_playbooks)
            avg_effectiveness = np.mean([p.effectiveness_score for p in recent_playbooks])
            
            # Get outcome data from feedback system
            successful_outcomes = 0
            total_outcomes = 0
            
            for playbook in recent_playbooks:
                if playbook.outcomes:
                    total_outcomes += len(playbook.outcomes)
                    successful_outcomes += sum(1 for outcome in playbook.outcomes 
                                             if outcome.get('result') in ['interested', 'meeting_scheduled', 'qualified'])
            
            success_rate = successful_outcomes / total_outcomes if total_outcomes > 0 else 0
            
            # Update template performance
            template.usage_count = total_uses
            template.success_rate = success_rate
            template.average_engagement = avg_effectiveness
            template.last_optimized = datetime.utcnow()
            
            # Extract effective/ineffective phrases
            await self.update_template_phrases(template, recent_playbooks)
            
            self.generation_stats['templates_optimized'] += 1
            
        finally:
            session_db.close()
    
    async def update_template_phrases(self, template: PlaybookTemplate, recent_playbooks: List[GeneratedPlaybook]):
        """Update effective/ineffective phrases based on performance"""
        
        effective_phrases = template.effective_phrases or []
        ineffective_phrases = template.ineffective_phrases or []
        
        # Analyze phrases from high-performing playbooks
        high_performing = [p for p in recent_playbooks if p.effectiveness_score > 0.7]
        low_performing = [p for p in recent_playbooks if p.effectiveness_score < 0.4]
        
        # Extract phrases using AI
        if high_performing:
            high_performing_scripts = [p.full_script for p in high_performing]
            new_effective = await self.extract_effective_phrases(high_performing_scripts)
            effective_phrases.extend(new_effective)
        
        if low_performing:
            low_performing_scripts = [p.full_script for p in low_performing]
            new_ineffective = await self.extract_ineffective_phrases(low_performing_scripts)
            ineffective_phrases.extend(new_ineffective)
        
        # Remove duplicates and limit size
        template.effective_phrases = list(set(effective_phrases))[-50:]  # Keep last 50
        template.ineffective_phrases = list(set(ineffective_phrases))[-25:]  # Keep last 25
    
    async def extract_effective_phrases(self, scripts: List[str]) -> List[str]:
        """Extract effective phrases from high-performing scripts"""
        
        combined_scripts = '\n'.join(scripts[:5])  # Limit input size
        
        prompt = f"""
        Analyze these high-performing sales scripts and extract the most effective phrases:
        
        {combined_scripts[:2000]}...
        
        Extract 5-10 specific phrases that likely contributed to success.
        Focus on:
        - Opening lines
        - Value propositions
        - Transition phrases
        - Closing statements
        
        Return as a JSON list of phrases.
        """
        
        try:
            response = await self.qdllm_engine.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing sales language patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            phrases = json.loads(response.choices[0].message.content)
            return phrases if isinstance(phrases, list) else []
        except:
            return []
    
    async def extract_ineffective_phrases(self, scripts: List[str]) -> List[str]:
        """Extract ineffective phrases from low-performing scripts"""
        
        combined_scripts = '\n'.join(scripts[:5])
        
        prompt = f"""
        Analyze these low-performing sales scripts and identify phrases that likely hurt performance:
        
        {combined_scripts[:2000]}...
        
        Extract 3-5 specific phrases that likely contributed to poor performance.
        Focus on:
        - Weak openings
        - Pushy language
        - Unclear value props
        - Poor transitions
        
        Return as a JSON list of phrases to avoid.
        """
        
        try:
            response = await self.qdllm_engine.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing sales language patterns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            phrases = json.loads(response.choices[0].message.content)
            return phrases if isinstance(phrases, list) else []
        except:
            return []
    
    async def initialize_default_templates(self):
        """Initialize default templates for common scenarios"""
        
        session_db = self.SessionLocal()
        
        try:
            # Check if templates already exist
            existing_count = session_db.query(PlaybookTemplate).count()
            if existing_count > 0:
                return
            
            # Create default templates
            default_templates = [
                {
                    "name": "cold_outreach_technology_c_level",
                    "playbook_type": PlaybookType.COLD_OUTREACH.value,
                    "industry_vertical": IndustryVertical.TECHNOLOGY.value,
                    "persona_type": PersonaType.C_LEVEL.value,
                    "company_size": "enterprise"
                },
                {
                    "name": "demo_presentation_healthcare_manager",
                    "playbook_type": PlaybookType.DEMO_PRESENTATION.value,
                    "industry_vertical": IndustryVertical.HEALTHCARE.value,
                    "persona_type": PersonaType.MANAGER.value,
                    "company_size": "mid_market"
                },
                {
                    "name": "objection_handling_finance_vp",
                    "playbook_type": PlaybookType.OBJECTION_HANDLING.value,
                    "industry_vertical": IndustryVertical.FINANCE.value,
                    "persona_type": PersonaType.VP_DIRECTOR.value,
                    "company_size": "enterprise"
                }
            ]
            
            for template_data in default_templates:
                template = await self.create_new_template(
                    template_data["playbook_type"],
                    template_data["industry_vertical"],
                    template_data["persona_type"],
                    template_data["company_size"]
                )
                logger.info(f"Created default template: {template.name}")
            
        finally:
            session_db.close()
    
    def get_generation_stats(self) -> Dict:
        """Get playbook generation statistics"""
        session_db = self.SessionLocal()
        
        try:
            total_playbooks = session_db.query(GeneratedPlaybook).count()
            total_templates = session_db.query(PlaybookTemplate).count()
            
            # Calculate average effectiveness
            recent_playbooks = session_db.query(GeneratedPlaybook).filter(
                GeneratedPlaybook.generation_timestamp >= datetime.utcnow() - timedelta(days=7)
            ).all()
            
            avg_effectiveness = np.mean([p.effectiveness_score for p in recent_playbooks]) if recent_playbooks else 0
            
            self.generation_stats.update({
                'total_playbooks_generated': total_playbooks,
                'total_templates': total_templates,
                'average_effectiveness': avg_effectiveness,
                'recent_playbooks_7d': len(recent_playbooks)
            })
            
            return self.generation_stats
        
        finally:
            session_db.close()

# FastAPI application
app = FastAPI(
    title="Dynamic Playbook Generator",
    description="Quantum-enhanced playbook generation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global playbook generator
playbook_generator = None

@app.on_event("startup")
async def startup_event():
    global playbook_generator
    
    import os
    playbook_generator = DynamicPlaybookGenerator(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    logger.info("Dynamic Playbook Generator started")

@app.post("/playbooks/generate", response_model=PlaybookResponse)
async def generate_playbook(request: PlaybookGenerationRequest):
    """Generate a personalized playbook"""
    try:
        response = await playbook_generator.generate_playbook(request)
        return response
    except Exception as e:
        logger.error(f"Error generating playbook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playbooks/{playbook_id}")
async def get_playbook(playbook_id: str):
    """Get a specific playbook"""
    session_db = playbook_generator.SessionLocal()
    
    try:
        playbook = session_db.query(GeneratedPlaybook).filter(
            GeneratedPlaybook.id == playbook_id
        ).first()
        
        if not playbook:
            raise HTTPException(status_code=404, detail="Playbook not found")
        
        return {
            'playbook_id': playbook.id,
            'script_sections': playbook.sections,
            'quantum_insights': playbook.quantum_insights,
            'effectiveness_score': playbook.effectiveness_score,
            'generated_at': playbook.generation_timestamp.isoformat()
        }
    
    finally:
        session_db.close()

@app.get("/templates")
async def list_templates():
    """List available playbook templates"""
    session_db = playbook_generator.SessionLocal()
    
    try:
        templates = session_db.query(PlaybookTemplate).order_by(
            PlaybookTemplate.success_rate.desc()
        ).all()
        
        return {
            'templates': [{
                'id': t.id,
                'name': t.name,
                'type': t.playbook_type,
                'industry': t.industry_vertical,
                'persona': t.persona_type,
                'success_rate': t.success_rate,
                'usage_count': t.usage_count
            } for t in templates]
        }
    
    finally:
        session_db.close()

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    return playbook_generator.get_generation_stats()

@app.post("/optimize")
async def trigger_optimization():
    """Manually trigger template optimization"""
    try:
        await playbook_generator.optimize_templates_daily()
        return {'status': 'optimization_completed'}
    except Exception as e:
        logger.error(f"Error in optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "dynamic_playbook_generator:app",
        host="0.0.0.0",
        port=8005,
        reload=True,
        log_level="info"
    )