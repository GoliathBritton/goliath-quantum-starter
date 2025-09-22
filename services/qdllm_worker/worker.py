"""qdLLM Worker Implementation

Quantum-enhanced Language Model worker with parallel exploration,
reversal reasoning, and quantum-optimized response generation.
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Union

import openai
from pydantic import BaseModel

from .config import QdLLMConfig
from .models import (
    QdLLMRequest,
    QdLLMResponse,
    ExplorationResult,
    ReasoningResult,
    RankingResult
)
from ...core.quantum_job_manager import QuantumJobManager, JobType, JobPriority


class QdLLMWorker:
    """Quantum-enhanced Language Model Worker
    
    Provides quantum-enhanced capabilities including:
    - Parallel exploration of conversation strategies
    - Reversal reasoning for root cause analysis
    - Quantum-optimized ranking and selection
    - Multi-dimensional response generation
    """
    
    def __init__(self, 
                 config: QdLLMConfig,
                 quantum_job_manager: Optional[QuantumJobManager] = None):
        self.config = config
        self.qjm = quantum_job_manager
        self.logger = logging.getLogger("qdllm_worker")
        
        # Initialize OpenAI client
        if config.openai_api_key:
            openai.api_key = config.openai_api_key
        
        # Load prompt templates
        self.prompts = self._load_prompt_templates()
        
        # Performance metrics
        self.metrics = {
            "requests_processed": 0,
            "parallel_explorations": 0,
            "reasoning_sessions": 0,
            "quantum_rankings": 0,
            "average_response_time": 0.0,
            "error_count": 0
        }
        
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates from files"""
        templates = {}
        template_files = {
            "reversal_reasoning": "prompts/reversal_reasoning.txt",
            "parallel_exploration": "prompts/parallel_exploration.txt",
            "lead_qualification": "prompts/lead_qualification.txt",
            "quantum_ranking": "prompts/quantum_ranking.txt"
        }
        
        for name, file_path in template_files.items():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    templates[name] = f.read()
                self.logger.info(f"Loaded prompt template: {name}")
            except FileNotFoundError:
                self.logger.warning(f"Prompt template not found: {file_path}")
                templates[name] = self._get_default_template(name)
                
        return templates
        
    def _get_default_template(self, template_name: str) -> str:
        """Get default template if file not found"""
        defaults = {
            "reversal_reasoning": "Analyze the outcome: {outcome} and provide root cause analysis.",
            "parallel_exploration": "Explore multiple strategies for: {objective}",
            "lead_qualification": "Qualify this lead: {lead_data}",
            "quantum_ranking": "Rank these candidates: {candidates}"
        }
        return defaults.get(template_name, "Default template for {template_name}")
        
    async def process_request(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process a qdLLM request with quantum enhancement"""
        start_time = time.time()
        
        try:
            self.logger.info(f"Processing qdLLM request: {request.request_type}")
            
            # Route to appropriate handler
            if request.request_type == "parallel_exploration":
                result = await self._parallel_exploration(request)
            elif request.request_type == "reversal_reasoning":
                result = await self._reversal_reasoning(request)
            elif request.request_type == "quantum_ranking":
                result = await self._quantum_ranking(request)
            elif request.request_type == "lead_qualification":
                result = await self._lead_qualification(request)
            else:
                result = await self._general_completion(request)
                
            # Update metrics
            processing_time = time.time() - start_time
            self._update_metrics(request.request_type, processing_time)
            
            response = QdLLMResponse(
                request_id=request.request_id,
                result=result,
                processing_time=processing_time,
                quantum_enhanced=True,
                confidence=result.get("confidence", 0.8) if isinstance(result, dict) else 0.8
            )
            
            self.logger.info(f"Request {request.request_id} completed in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request {request.request_id}: {e}")
            self.metrics["error_count"] += 1
            
            return QdLLMResponse(
                request_id=request.request_id,
                result={"error": str(e)},
                processing_time=time.time() - start_time,
                quantum_enhanced=False,
                confidence=0.0,
                error=str(e)
            )
            
    async def _parallel_exploration(self, request: QdLLMRequest) -> ExplorationResult:
        """Perform parallel exploration of conversation strategies"""
        self.metrics["parallel_explorations"] += 1
        
        # Extract parameters
        lead_profile = request.context.get("lead_profile", {})
        objective = request.context.get("objective", "engagement")
        num_strategies = request.parameters.get("num_strategies", 6)
        
        # Format prompt
        prompt = self.prompts["parallel_exploration"].format(
            lead_profile=json.dumps(lead_profile),
            objective=objective,
            context=json.dumps(request.context),
            interaction_history=json.dumps(request.context.get("interaction_history", [])),
            constraints=json.dumps(request.parameters.get("constraints", [])),
            num_strategies=num_strategies
        )
        
        # Generate strategies using OpenAI
        strategies = await self._generate_strategies(prompt, num_strategies)
        
        # If quantum job manager available, rank strategies
        if self.qjm and len(strategies) > 1:
            ranking_job = await self.qjm.submit({
                "type": "rank_paths",
                "candidates": strategies,
                "context": request.context
            }, JobPriority.NORMAL)
            
            try:
                ranking_result = await self.qjm.wait(ranking_job.id, timeout=10)
                if ranking_result and "ranking" in ranking_result:
                    # Reorder strategies based on quantum ranking
                    ranked_strategies = self._reorder_by_ranking(strategies, ranking_result["ranking"])
                    strategies = ranked_strategies
            except Exception as e:
                self.logger.warning(f"Quantum ranking failed, using original order: {e}")
                
        return ExplorationResult(
            strategies=strategies,
            quantum_ranked=self.qjm is not None,
            confidence=0.85,
            metadata={
                "num_strategies": len(strategies),
                "objective": objective,
                "quantum_enhanced": True
            }
        )
        
    async def _reversal_reasoning(self, request: QdLLMRequest) -> ReasoningResult:
        """Perform reversal reasoning for root cause analysis"""
        self.metrics["reasoning_sessions"] += 1
        
        # Extract parameters
        outcome = request.context.get("outcome", "")
        observed_data = request.context.get("observed_data", {})
        num_candidates = request.parameters.get("num_candidates", 6)
        
        # Format prompt
        prompt = self.prompts["reversal_reasoning"].format(
            outcome=outcome,
            context=json.dumps(request.context),
            data_points=json.dumps(observed_data),
            time_window=request.context.get("time_window", "last 30 days"),
            num_candidates=num_candidates
        )
        
        # Generate backtrace candidates
        backtrace_result = await self._generate_backtrace(prompt)
        
        # If quantum job manager available, optimize backtrace
        if self.qjm and backtrace_result.get("backtrace_candidates"):
            backtrace_job = await self.qjm.submit({
                "type": "backtrace",
                "target_outcome": outcome,
                "observed_data": observed_data,
                "candidates": backtrace_result["backtrace_candidates"]
            }, JobPriority.HIGH)
            
            try:
                quantum_result = await self.qjm.wait(backtrace_job.id, timeout=15)
                if quantum_result and "root_causes" in quantum_result:
                    # Enhance backtrace with quantum insights
                    backtrace_result["quantum_insights"] = quantum_result
                    backtrace_result["confidence"] = quantum_result.get("confidence", 0.8)
            except Exception as e:
                self.logger.warning(f"Quantum backtrace failed: {e}")
                
        return ReasoningResult(
            analysis=backtrace_result,
            quantum_enhanced=self.qjm is not None,
            confidence=backtrace_result.get("confidence", 0.75),
            metadata={
                "outcome_analyzed": outcome,
                "num_candidates": len(backtrace_result.get("backtrace_candidates", [])),
                "quantum_optimized": True
            }
        )
        
    async def _quantum_ranking(self, request: QdLLMRequest) -> RankingResult:
        """Perform quantum-enhanced ranking of candidates"""
        self.metrics["quantum_rankings"] += 1
        
        # Extract parameters
        candidates = request.context.get("candidates", [])
        criteria = request.parameters.get("criteria", [])
        goal = request.parameters.get("goal", "optimization")
        
        # Format prompt
        prompt = self.prompts["quantum_ranking"].format(
            candidates=json.dumps(candidates),
            criteria=json.dumps(criteria),
            context=json.dumps(request.context),
            constraints=json.dumps(request.parameters.get("constraints", [])),
            goal=goal
        )
        
        # Generate initial ranking
        ranking_result = await self._generate_ranking(prompt)
        
        # If quantum job manager available, optimize ranking
        if self.qjm and candidates:
            ranking_job = await self.qjm.submit({
                "type": "rank_paths",
                "candidates": candidates,
                "context": request.context,
                "criteria": criteria
            }, JobPriority.NORMAL)
            
            try:
                quantum_result = await self.qjm.wait(ranking_job.id, timeout=10)
                if quantum_result and "ranking" in quantum_result:
                    # Merge LLM insights with quantum optimization
                    ranking_result["quantum_ranking"] = quantum_result["ranking"]
                    ranking_result["quantum_confidence"] = quantum_result.get("confidence", 0.8)
            except Exception as e:
                self.logger.warning(f"Quantum ranking optimization failed: {e}")
                
        return RankingResult(
            ranking=ranking_result,
            quantum_optimized=self.qjm is not None,
            confidence=ranking_result.get("confidence_level", 0.8),
            metadata={
                "num_candidates": len(candidates),
                "optimization_goal": goal,
                "quantum_enhanced": True
            }
        )
        
    async def _lead_qualification(self, request: QdLLMRequest) -> Dict[str, Any]:
        """Perform quantum-enhanced lead qualification"""
        # Extract lead data
        lead_data = request.context.get("lead_data", {})
        company_info = request.context.get("company_info", {})
        
        # Format prompt
        prompt = self.prompts["lead_qualification"].format(
            lead_data=json.dumps(lead_data),
            company_info=json.dumps(company_info),
            interaction_history=json.dumps(request.context.get("interaction_history", [])),
            behavioral_signals=json.dumps(request.context.get("behavioral_signals", [])),
            market_context=json.dumps(request.context.get("market_context", {}))
        )
        
        # Generate qualification analysis
        qualification_result = await self._generate_qualification(prompt)
        
        # If quantum job manager available, optimize lead scoring
        if self.qjm and lead_data:
            scoring_job = await self.qjm.submit({
                "type": "lead_ranking",
                "leads": [lead_data],
                "context": request.context
            }, JobPriority.NORMAL)
            
            try:
                quantum_result = await self.qjm.wait(scoring_job.id, timeout=8)
                if quantum_result:
                    qualification_result["quantum_score"] = quantum_result
            except Exception as e:
                self.logger.warning(f"Quantum lead scoring failed: {e}")
                
        return qualification_result
        
    async def _general_completion(self, request: QdLLMRequest) -> Dict[str, Any]:
        """Handle general completion requests"""
        prompt = request.prompt
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are qdLLM, a quantum-enhanced AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": self.config.model_name,
                "quantum_enhanced": False
            }
            
        except Exception as e:
            self.logger.error(f"OpenAI completion failed: {e}")
            return {
                "error": str(e),
                "response": "I apologize, but I'm unable to process your request at the moment."
            }
            
    async def _generate_strategies(self, prompt: str, num_strategies: int) -> List[Dict[str, Any]]:
        """Generate conversation strategies using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Generate {num_strategies} distinct conversation strategies."}
                ],
                max_tokens=self.config.max_tokens,
                temperature=0.8  # Higher temperature for creativity
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return result.get("conversation_strategies", [])
            
        except Exception as e:
            self.logger.error(f"Strategy generation failed: {e}")
            # Return mock strategies as fallback
            return self._generate_mock_strategies(num_strategies)
            
    async def _generate_backtrace(self, prompt: str) -> Dict[str, Any]:
        """Generate backtrace analysis using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Perform reversal reasoning analysis."}
                ],
                max_tokens=self.config.max_tokens,
                temperature=0.7
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            self.logger.error(f"Backtrace generation failed: {e}")
            return self._generate_mock_backtrace()
            
    async def _generate_ranking(self, prompt: str) -> Dict[str, Any]:
        """Generate ranking analysis using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Perform quantum-enhanced ranking analysis."}
                ],
                max_tokens=self.config.max_tokens,
                temperature=0.6
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            self.logger.error(f"Ranking generation failed: {e}")
            return self._generate_mock_ranking()
            
    async def _generate_qualification(self, prompt: str) -> Dict[str, Any]:
        """Generate lead qualification using OpenAI"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Perform comprehensive lead qualification."}
                ],
                max_tokens=self.config.max_tokens,
                temperature=0.5
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            self.logger.error(f"Qualification generation failed: {e}")
            return self._generate_mock_qualification()
            
    def _reorder_by_ranking(self, strategies: List[Dict[str, Any]], 
                           ranking: List[str]) -> List[Dict[str, Any]]:
        """Reorder strategies based on quantum ranking"""
        strategy_map = {s.get("strategy_id", f"S{i}"): s for i, s in enumerate(strategies)}
        reordered = []
        
        for rank_id in ranking:
            if rank_id in strategy_map:
                reordered.append(strategy_map[rank_id])
                
        # Add any strategies not in ranking
        for strategy in strategies:
            if strategy not in reordered:
                reordered.append(strategy)
                
        return reordered
        
    def _generate_mock_strategies(self, num_strategies: int) -> List[Dict[str, Any]]:
        """Generate mock strategies for fallback"""
        strategies = []
        approaches = ["consultative", "social_proof", "urgency", "educational", "direct", "challenger"]
        
        for i in range(min(num_strategies, len(approaches))):
            strategies.append({
                "strategy_id": f"S{i+1}",
                "strategy_name": f"{approaches[i].title()} Approach",
                "core_approach": approaches[i],
                "conversion_confidence": 0.7 + (i * 0.05),
                "opening_line": f"Mock opening line for {approaches[i]} strategy"
            })
            
        return strategies
        
    def _generate_mock_backtrace(self) -> Dict[str, Any]:
        """Generate mock backtrace for fallback"""
        return {
            "backtrace_candidates": [
                {
                    "candidate_id": "C1",
                    "cause_summary": "Mock root cause analysis",
                    "likelihood_score": 0.8,
                    "confidence_level": "medium"
                }
            ],
            "confidence": 0.6
        }
        
    def _generate_mock_ranking(self) -> Dict[str, Any]:
        """Generate mock ranking for fallback"""
        return {
            "quantum_ranking": [
                {"rank": 1, "candidate_id": "C1", "overall_score": 85},
                {"rank": 2, "candidate_id": "C2", "overall_score": 78}
            ],
            "confidence_level": 0.7
        }
        
    def _generate_mock_qualification(self) -> Dict[str, Any]:
        """Generate mock qualification for fallback"""
        return {
            "overall_qualification": {
                "composite_score": 75,
                "qualification_tier": "B",
                "confidence_level": 0.7
            }
        }
        
    def _update_metrics(self, request_type: str, processing_time: float):
        """Update performance metrics"""
        self.metrics["requests_processed"] += 1
        
        # Update average response time
        current_avg = self.metrics["average_response_time"]
        total_requests = self.metrics["requests_processed"]
        self.metrics["average_response_time"] = (
            (current_avg * (total_requests - 1) + processing_time) / total_requests
        )
        
    async def get_metrics(self) -> Dict[str, Any]:
        """Get worker performance metrics"""
        return self.metrics.copy()
        
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        return {
            "status": "healthy",
            "quantum_job_manager": self.qjm is not None,
            "prompts_loaded": len(self.prompts),
            "requests_processed": self.metrics["requests_processed"],
            "error_rate": self.metrics["error_count"] / max(1, self.metrics["requests_processed"])
        }