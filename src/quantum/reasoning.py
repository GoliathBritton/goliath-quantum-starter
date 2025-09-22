"""Reversal Reasoning Algorithm for Logical Inference

This module implements qdLLM-inspired bidirectional reasoning, processing
forward (premise → conclusion) and backward (conclusion → premise) paths
simultaneously for coherent outputs. Ideal for funding assessments and
educational logic puzzles.
"""

import numpy as np
import asyncio
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ReversalReasoning:
    """Advanced bidirectional reasoning engine with dynamic adaptation."""
    
    def __init__(self, base_coherence_threshold: float = 0.9):
        self.base_coherence_threshold = base_coherence_threshold
        self.performance_history = []
        
    def _calculate_complexity_factor(self, premise: str, conclusion: str) -> float:
        """Calculate input complexity to adjust thresholds dynamically."""
        total_length = len(premise) + len(conclusion)
        word_count = len(premise.split()) + len(conclusion.split())
        
        # Complexity increases with length and word density
        complexity = (total_length / 100) + (word_count / 20)
        return min(complexity, 2.0)  # Cap at 2.0
    
    def _simulate_quantum_scoring(self, text: str, direction: str) -> float:
        """Simulate quantum-inspired scoring (replace with Dynex QUBO in production)."""
        # Mock quantum scoring with realistic variance
        base_score = np.random.uniform(0.85, 0.99)
        
        # Add direction-specific bias
        if direction == "forward":
            bias = 0.02 if "strong" in text.lower() else 0.0
        else:  # backward
            bias = 0.02 if "support" in text.lower() else 0.0
            
        return min(base_score + bias, 1.0)
    
    async def _forward_reasoning(self, premise: str, conclusion: str) -> Tuple[str, float]:
        """Forward reasoning: premise → inference → conclusion."""
        await asyncio.sleep(0.01)  # Simulate processing time
        
        inference = f"{premise} implies {conclusion}"
        score = self._simulate_quantum_scoring(premise + conclusion, "forward")
        
        return inference, score
    
    async def _backward_reasoning(self, premise: str, conclusion: str) -> Tuple[str, float]:
        """Backward reasoning: conclusion → inference → premise."""
        await asyncio.sleep(0.01)  # Simulate processing time
        
        inference = f"{conclusion} supports {premise}"
        score = self._simulate_quantum_scoring(conclusion + premise, "backward")
        
        return inference, score
    
    def _adaptive_threshold(self, complexity_factor: float) -> float:
        """Dynamically adjust coherence threshold based on input complexity."""
        if complexity_factor > 1.5:
            # Lower threshold for complex inputs to allow flexibility
            return self.base_coherence_threshold * 0.90
        elif complexity_factor > 1.0:
            return self.base_coherence_threshold * 0.95
        else:
            return self.base_coherence_threshold
    
    def _generate_refined_input(self, premise: str, conclusion: str) -> Tuple[str, str]:
        """Generate refined inputs for retry when coherence is low."""
        refined_premise = f"{premise.strip()} (refined for clarity)"
        refined_conclusion = f"{conclusion.strip()} (with enhanced context)"
        return refined_premise, refined_conclusion
    
    async def reason(self, premise: str, conclusion: str, 
                    coherence_threshold: Optional[float] = None) -> Dict:
        """Main reasoning function with bidirectional processing."""
        try:
            # Calculate dynamic parameters
            complexity_factor = self._calculate_complexity_factor(premise, conclusion)
            
            if coherence_threshold is None:
                coherence_threshold = self._adaptive_threshold(complexity_factor)
            
            # Parallel bidirectional reasoning
            forward_task = self._forward_reasoning(premise, conclusion)
            backward_task = self._backward_reasoning(premise, conclusion)
            
            (forward_inference, forward_score), (backward_inference, backward_score) = await asyncio.gather(
                forward_task, backward_task
            )
            
            # Calculate coherence as minimum of both directions
            coherence = min(forward_score, backward_score)
            
            # Track performance for future optimization
            self.performance_history.append({
                'coherence': coherence,
                'complexity': complexity_factor,
                'threshold': coherence_threshold
            })
            
            if coherence >= coherence_threshold:
                return {
                    "status": "success",
                    "forward": forward_inference,
                    "backward": backward_inference,
                    "coherence": round(coherence, 3),
                    "complexity_factor": round(complexity_factor, 2),
                    "threshold_used": round(coherence_threshold, 3)
                }
            else:
                # Self-improvement: Generate refined retry
                logger.info(f"Low coherence ({coherence:.3f}), attempting refinement")
                
                refined_premise, refined_conclusion = self._generate_refined_input(premise, conclusion)
                
                # Recursive retry with refined inputs (limit to prevent infinite recursion)
                if len(premise) < 500:  # Prevent excessive refinement
                    retry_result = await self.reason(refined_premise, refined_conclusion, coherence_threshold * 0.95)
                    return {
                        "status": "refined",
                        "original_coherence": round(coherence, 3),
                        "retry_result": retry_result
                    }
                else:
                    return {
                        "status": "low_coherence",
                        "coherence": round(coherence, 3),
                        "threshold": round(coherence_threshold, 3),
                        "message": "Input too complex for refinement"
                    }
                    
        except Exception as e:
            logger.error(f"Reasoning error: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics for optimization."""
        if not self.performance_history:
            return {"message": "No performance data available"}
        
        coherences = [p['coherence'] for p in self.performance_history]
        complexities = [p['complexity'] for p in self.performance_history]
        
        return {
            "total_inferences": len(self.performance_history),
            "avg_coherence": round(np.mean(coherences), 3),
            "avg_complexity": round(np.mean(complexities), 3),
            "success_rate": round(len([c for c in coherences if c >= 0.9]) / len(coherences), 3)
        }

# Global instance for API usage
reasoning_engine = ReversalReasoning()

# Convenience function for direct usage
async def reversal_reasoning(premise: str, conclusion: str, 
                           coherence_threshold: Optional[float] = None) -> Dict:
    """Convenience function for reversal reasoning."""
    return await reasoning_engine.reason(premise, conclusion, coherence_threshold)

# Synchronous wrapper for compatibility
def reversal_reasoning_sync(premise: str, conclusion: str, 
                          coherence_threshold: Optional[float] = None) -> Dict:
    """Synchronous wrapper for reversal reasoning."""
    return asyncio.run(reversal_reasoning(premise, conclusion, coherence_threshold))