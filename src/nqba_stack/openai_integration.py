"""
Enhanced OpenAI Integration for NQBA Stack
==========================================
- Modern OpenAI SDK v1.0+ integration
- Streaming responses and function calling
- Quantum enhancement via qdLLM pipeline
- MCP tool integration
- Fallback and error handling
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, AsyncGenerator, Union
from dataclasses import dataclass, field
from datetime import datetime
import openai
from openai import AsyncOpenAI
import tiktoken

from .qdllm import qdllm
from .core.settings import NQBASettings

logger = logging.getLogger(__name__)


@dataclass
class OpenAIRequest:
    """Enhanced OpenAI request with quantum options"""

    prompt: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[str, Dict[str, str]]] = None
    use_quantum_enhancement: bool = True
    quantum_context: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class OpenAIResponse:
    """Enhanced OpenAI response with quantum metadata"""

    content: str
    model: str
    usage: Dict[str, Any]
    quantum_enhanced: bool = False
    quantum_metadata: Optional[Dict[str, Any]] = None
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


class EnhancedOpenAIIntegration:
    """Enhanced OpenAI integration with quantum capabilities"""

    def __init__(self, api_key: Optional[str] = None):
        self.settings = NQBASettings()
        self.api_key = api_key or self.settings.openai_api_key

        if not self.api_key:
            logger.warning(
                "OpenAI API key not configured - using quantum fallback only"
            )
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)

        self.tokenizer = self._get_tokenizer()
        self.quantum_enhancement_enabled = True

    def _get_tokenizer(self):
        """Get appropriate tokenizer for the model"""
        try:
            return tiktoken.encoding_for_model("gpt-4")
        except:
            return tiktoken.get_encoding("cl100k_base")

    async def generate(
        self, request: OpenAIRequest
    ) -> Union[OpenAIResponse, AsyncGenerator[OpenAIResponse, None]]:
        """Generate response with quantum enhancement"""

        start_time = datetime.now()

        if request.stream:
            return self._generate_stream(request, start_time)
        else:
            return await self._generate_single(request, start_time)

    async def _generate_single(
        self, request: OpenAIRequest, start_time: datetime
    ) -> OpenAIResponse:
        """Generate single response"""

        try:
            # Try OpenAI first if available
            if self.client and not request.use_quantum_enhancement:
                response = await self._call_openai(request)
                return OpenAIResponse(
                    content=response.choices[0].message.content,
                    model=response.model,
                    usage=response.usage.model_dump(),
                    quantum_enhanced=False,
                    processing_time=(datetime.now() - start_time).total_seconds(),
                )

            # Use quantum-enhanced generation
            quantum_response = await self._generate_quantum_enhanced(request)

            processing_time = (datetime.now() - start_time).total_seconds()

            return OpenAIResponse(
                content=quantum_response["content"],
                model=f"qdllm-{request.model}",
                usage=quantum_response.get("usage", {}),
                quantum_enhanced=True,
                quantum_metadata=quantum_response.get("quantum_metadata"),
                processing_time=processing_time,
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            # Fallback to quantum-only
            return await self._quantum_fallback(request, start_time)

    async def _generate_stream(
        self, request: OpenAIRequest, start_time: datetime
    ) -> AsyncGenerator[OpenAIResponse, None]:
        """Generate streaming response"""

        try:
            if self.client and not request.use_quantum_enhancement:
                async for chunk in self._stream_openai(request):
                    yield chunk
                return

            # Quantum streaming (simulated for now)
            quantum_response = await self._generate_quantum_enhanced(request)
            content = quantum_response["content"]

            # Simulate streaming by yielding chunks
            chunk_size = 50
            for i in range(0, len(content), chunk_size):
                chunk = content[i : i + chunk_size]
                yield OpenAIResponse(
                    content=chunk,
                    model=f"qdllm-{request.model}",
                    usage={"tokens": len(chunk)},
                    quantum_enhanced=True,
                    processing_time=(datetime.now() - start_time).total_seconds(),
                )
                await asyncio.sleep(0.1)  # Simulate streaming delay

        except Exception as e:
            logger.error(f"Streaming generation failed: {e}")
            # Fallback
            fallback = await self._quantum_fallback(request, start_time)
            yield fallback

    async def _call_openai(self, request: OpenAIRequest):
        """Call OpenAI API directly"""
        messages = [{"role": "user", "content": request.prompt}]

        kwargs = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        if request.functions:
            kwargs["functions"] = request.functions
            kwargs["function_call"] = request.function_call

        return await self.client.chat.completions.create(**kwargs)

    async def _stream_openai(self, request: OpenAIRequest):
        """Stream from OpenAI API"""
        messages = [{"role": "user", "content": request.prompt}]

        kwargs = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": True,
        }

        async for chunk in self.client.chat.completions.create(**kwargs):
            if chunk.choices[0].delta.content:
                yield OpenAIResponse(
                    content=chunk.choices[0].delta.content,
                    model=chunk.model,
                    usage={"tokens": 1},
                    quantum_enhanced=False,
                    processing_time=(datetime.now() - datetime.now()).total_seconds(),
                )

    async def _generate_quantum_enhanced(
        self, request: OpenAIRequest
    ) -> Dict[str, Any]:
        """Generate quantum-enhanced response using qdLLM"""

        # Prepare quantum context
        quantum_context = request.quantum_context or {}
        quantum_context.update(
            {
                "openai_model": request.model,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
                "user_id": request.user_id,
                "session_id": request.session_id,
            }
        )

        # Generate via qdLLM
        result = await qdllm.generate(
            prompt=request.prompt,
            context=json.dumps(quantum_context),
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            use_quantum_enhancement=True,
            task="text_generation",
            algorithm="qaoa",
        )

        return {
            "content": result.get("generated_text", result.get("result", "")),
            "usage": result.get("usage", {}),
            "quantum_metadata": {
                "algorithm": "qaoa",
                "quantum_enhancement": True,
                "dynex_used": result.get("dynex_used", False),
            },
        }

    async def _quantum_fallback(
        self, request: OpenAIRequest, start_time: datetime
    ) -> OpenAIResponse:
        """Fallback to quantum-only generation"""

        quantum_response = await self._generate_quantum_enhanced(request)

        return OpenAIResponse(
            content=quantum_response["content"],
            model="qdllm-fallback",
            usage=quantum_response.get("usage", {}),
            quantum_enhanced=True,
            quantum_metadata=quantum_response.get("quantum_metadata"),
            processing_time=(datetime.now() - start_time).total_seconds(),
        )

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))

    async def get_embeddings(
        self, text: str, model: str = "text-embedding-3-small"
    ) -> List[float]:
        """Get embeddings with quantum enhancement"""

        if self.client and not self.quantum_enhancement_enabled:
            response = await self.client.embeddings.create(model=model, input=text)
            return response.data[0].embedding

        # Quantum-enhanced embeddings via qdLLM
        result = await qdllm.generate(
            prompt=f"Generate embeddings for: {text}",
            task="embedding_generation",
            use_quantum_enhancement=True,
        )

        # Parse embeddings from result
        embeddings = result.get("embeddings", [])
        if not embeddings and isinstance(result.get("result"), list):
            embeddings = result["result"]

        return embeddings if embeddings else [0.0] * 1536  # Default embedding size


# Global instance
openai_integration = EnhancedOpenAIIntegration()
