"""
Quantum-driven LLM (qdLLM) and QNLP Pipeline
-------------------------------------------
- Uses Dynex as quantum backend for NLP/LLM tasks
- Designed for integration with DynexSDK and QNLP research
- All LLM calls routed through this module
"""

import asyncio
import logging
from typing import Dict, Any, Optional

from .qnlp import qnlp
from .dynex_client import get_dynex_client
from .quantum_diffusion import quantum_diffusion
from .qtransformer import qtransformer

logger = logging.getLogger("qdllm")


class QDLLM:
    def __init__(self, dynex_api_key: Optional[str] = None):
        self.dynex_api_key = dynex_api_key or "demo"
        self.dynex_client = None
        self.openai_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize DynexSDK and OpenAI clients."""
        # Initialize Dynex client
        try:
            from .dynex_client import DynexClient
            self.dynex_client = DynexClient(self.dynex_api_key)
            logger.info("QDLLM: DynexSDK client initialized")
        except Exception as e:
            logger.warning(f"QDLLM: Failed to initialize DynexSDK client: {e}")
            self.dynex_client = None
        
        # Initialize OpenAI client for classical fallback
        try:
            import openai
            import os
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = openai.AsyncOpenAI(api_key=api_key)
                logger.info("QDLLM: OpenAI client initialized")
            else:
                logger.warning("QDLLM: OpenAI API key not found")
                self.openai_client = None
        except ImportError:
            logger.warning("QDLLM: OpenAI library not available")
            self.openai_client = None
        except Exception as e:
            logger.warning(f"QDLLM: Failed to initialize OpenAI client: {e}")
            self.openai_client = None

    async def generate(
        self,
        prompt: str,
        context: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: int = 256,
        use_quantum_enhancement: bool = True,
        task: str = "text_classification",
        labels: Optional[list] = None,
        algorithm: str = "qaoa",
        parameters: Optional[dict] = None,
        mode: str = "qdllm",
    ) -> Dict[str, Any]:
        """
        Quantum-enhanced LLM/NLP using QNLP pipeline and Dynex QUBO
        - task: NLP task (e.g., text_classification, sentiment, ner, summarization)
        - labels: possible output labels (for classification)
        - algorithm: QAOA, VQE, custom, etc.
        - parameters: algorithm-specific params
        """
        logger.info(
            f"QD-LLM generate: quantum={use_quantum_enhancement}, task={task}, algo={algorithm}"
        )
        dynex = get_dynex_client()
        if use_quantum_enhancement:
            if mode == "qdllm":
                # Quantum Diffusion LLM pipeline
                tokens = prompt.split() if prompt else []
                tokens = [
                    t if i % 2 == 0 else "[MASK]" for i, t in enumerate(tokens)
                ]  # Example: mask every other token
                generated = await quantum_diffusion.generate(
                    tokens,
                    steps=5,
                    quantum_steps=3,
                    algorithm=algorithm,
                    parameters=parameters,
                )
                return {"text": " ".join(generated), "pipeline": "qdllm"}
            elif mode == "qtransformer":
                # Quantum Transformer pipeline
                tokens = prompt.split() if prompt else []
                generated = await qtransformer.generate(
                    tokens, heads=8, algorithm="qtransform", parameters=parameters
                )
                return {"text": " ".join(generated), "pipeline": "qtransformer"}
            # QNLP tasks
            if task == "text_classification" and labels:
                qubo = qnlp.text_classification_to_qubo(prompt, labels)
                qubo_result = await dynex.submit_qubo(
                    qubo, algorithm=algorithm, parameters=parameters
                )
                decoded = qnlp.decode_qubo_result(qubo_result, labels)
                return {"text": decoded, "qubo_result": qubo_result, "pipeline": "qnlp"}
            elif task == "sentiment":
                qubo = qnlp.sentiment_to_qubo(prompt)
                qubo_result = await dynex.submit_qubo(
                    qubo, algorithm=algorithm, parameters=parameters
                )
                decoded = qnlp.decode_sentiment_result(qubo_result)
                return {"text": decoded, "qubo_result": qubo_result, "pipeline": "qnlp"}
            elif task == "ner" and labels:
                qubo = qnlp.ner_to_qubo(prompt, labels)
                qubo_result = await dynex.submit_qubo(
                    qubo, algorithm=algorithm, parameters=parameters
                )
                decoded = qnlp.decode_ner_result(qubo_result, labels)
                return {"text": decoded, "qubo_result": qubo_result, "pipeline": "qnlp"}
            elif task == "summarization":
                qubo = qnlp.summarization_to_qubo(prompt)
                qubo_result = await dynex.submit_qubo(
                    qubo, algorithm=algorithm, parameters=parameters
                )
                sentences = prompt.split(".")
                decoded = qnlp.decode_summarization_result(qubo_result, sentences)
                return {"text": decoded, "qubo_result": qubo_result, "pipeline": "qnlp"}
            else:
                await asyncio.sleep(0.2)
                return {
                    "text": f"[Dynex QNLP output for: {prompt}]",
                    "pipeline": "qnlp",
                }
        else:
            # Fallback to classical LLM (OpenAI, etc.)
            return await self._classical_llm_fallback(
                prompt, context, temperature, max_tokens, task
            )
    
    async def _classical_llm_fallback(
        self, 
        prompt: str, 
        context: Optional[str] = None, 
        temperature: float = 1.0, 
        max_tokens: int = 256,
        task: str = "text_classification"
    ) -> Dict[str, Any]:
        """Fallback to classical LLM when quantum enhancement is disabled."""
        if self.openai_client:
            try:
                # Construct the full prompt
                full_prompt = prompt
                if context:
                    full_prompt = f"Context: {context}\n\nPrompt: {prompt}"
                
                # Add task-specific instructions
                if task == "text_classification":
                    full_prompt = f"Classify the following text:\n{full_prompt}"
                elif task == "sentiment":
                    full_prompt = f"Analyze the sentiment of the following text:\n{full_prompt}"
                elif task == "ner":
                    full_prompt = f"Extract named entities from the following text:\n{full_prompt}"
                elif task == "summarization":
                    full_prompt = f"Summarize the following text:\n{full_prompt}"
                
                # Call OpenAI API
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                result_text = response.choices[0].message.content.strip()
                logger.info(f"Classical LLM response generated for task: {task}")
                
                return {
                    "text": result_text,
                    "pipeline": "classical_llm",
                    "model": "gpt-3.5-turbo",
                    "task": task
                }
                
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {e}")
                return {
                    "text": f"[Error: Classical LLM failed - {str(e)}]",
                    "pipeline": "error",
                    "task": task
                }
        else:
            # Mock response when no LLM is available
            await asyncio.sleep(0.1)
            return {
                "text": f"[Mock Classical LLM output for task '{task}': {prompt}]",
                "pipeline": "mock_classical",
                "task": task
            }


# Singleton for handler use
qdllm = QDLLM()
