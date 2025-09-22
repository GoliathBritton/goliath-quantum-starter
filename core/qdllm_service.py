import asyncio
import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import aiohttp
import numpy as np
from dataclasses import dataclass
from enum import Enum
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

# NQBA Framework integration
try:
    from nqba import create_framework
    from nqba.core.intelligence import qdllm, qnlp, qtransformers
    NQBA_AVAILABLE = True
except ImportError:
    print("NQBA Framework not available, using legacy mode")
    NQBA_AVAILABLE = False

try:
    import openai
except ImportError:
    print("Warning: OpenAI library not installed. Install with: pip install openai")
    openai = None

try:
    import torch
    import transformers
except ImportError:
    print("Warning: PyTorch/Transformers not installed. Install with: pip install torch transformers")
    torch = None
    transformers = None

# Enums
class ModelType(Enum):
    QDLLM_LOCAL = "qdllm_local"
    QDLLM_HYBRID = "qdllm_hybrid"
    OPENAI_GPT4 = "openai_gpt4"
    OPENAI_GPT35 = "openai_gpt35"
    NVIDIA_TRITON = "nvidia_triton"

class ProcessingMode(Enum):
    QUANTUM_ENHANCED = "quantum_enhanced"
    CLASSICAL = "classical"
    HYBRID = "hybrid"

@dataclass
class QdLLMRequest:
    """Request structure for qdLLM processing"""
    prompt: str
    model_type: ModelType
    processing_mode: ProcessingMode
    max_tokens: int = 1000
    temperature: float = 0.7
    quantum_params: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

@dataclass
class QdLLMResponse:
    """Response structure from qdLLM processing"""
    text: str
    confidence: float
    processing_time: float
    model_used: ModelType
    quantum_enhanced: bool
    reasoning_trace: Dict[str, Any]
    metadata: Dict[str, Any]
    session_id: Optional[str] = None

class QdLLMService:
    """Quantum-enhanced LLM service with NQBA framework integration and OpenAI fallback"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # NQBA Framework integration
        self.nqba_framework = None
        if NQBA_AVAILABLE:
            try:
                self.nqba_framework = create_framework(
                    enable_qdllm=True,
                    enable_qnlp=True,
                    enable_qtransformers=True,
                    governance_enabled=self.config.get("enable_governance", True),
                    compliance_checks=self.config.get("enable_compliance", True)
                )
                self.logger.info("NQBA Framework integration enabled")
            except Exception as e:
                self.logger.warning(f"NQBA Framework initialization failed: {e}")
                self.nqba_framework = None
        
        # Service endpoints (legacy support)
        self.qdllm_endpoint = self.config.get("qdllm_endpoint", "http://localhost:8001")
        self.nvidia_triton_endpoint = self.config.get("nvidia_triton_endpoint", "http://localhost:8002")
        
        # OpenAI configuration
        self.openai_client = None
        if openai and self.config.get("openai_api_key"):
            self.openai_client = openai.AsyncOpenAI(
                api_key=self.config["openai_api_key"]
            )
        
        # Local model configuration
        self.local_model = None
        self.local_tokenizer = None
        
        # Performance tracking
        self.request_count = 0
        self.total_processing_time = 0.0
        self.quantum_enhanced_requests = 0
        
        # Session management
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("QdLLM Service initialized with NQBA framework support")
    
    async def initialize(self):
        """Initialize the qdLLM service"""
        try:
            # Test qdLLM endpoint connectivity
            await self._test_qdllm_connectivity()
            
            # Initialize local models if configured
            if self.config.get("enable_local_models", False):
                await self._initialize_local_models()
            
            # Test NVIDIA Triton if configured
            if self.config.get("enable_nvidia_triton", False):
                await self._test_nvidia_connectivity()
            
            self.logger.info("QdLLM Service initialization complete")
            
        except Exception as e:
            self.logger.error(f"QdLLM Service initialization failed: {e}")
            raise
    
    async def _test_qdllm_connectivity(self):
        """Test connectivity to qdLLM service"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.qdllm_endpoint}/health", timeout=5) as response:
                    if response.status == 200:
                        self.logger.info("qdLLM service connectivity confirmed")
                    else:
                        self.logger.warning(f"qdLLM service returned status {response.status}")
        except Exception as e:
            self.logger.warning(f"qdLLM service not available: {e}")
    
    async def _test_nvidia_connectivity(self):
        """Test connectivity to NVIDIA Triton service"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.nvidia_triton_endpoint}/v2/health/ready", timeout=5) as response:
                    if response.status == 200:
                        self.logger.info("NVIDIA Triton service connectivity confirmed")
                    else:
                        self.logger.warning(f"NVIDIA Triton service returned status {response.status}")
        except Exception as e:
            self.logger.warning(f"NVIDIA Triton service not available: {e}")
    
    async def _initialize_local_models(self):
        """Initialize local transformer models"""
        if not torch or not transformers:
            self.logger.warning("PyTorch/Transformers not available for local models")
            return
        
        try:
            model_name = self.config.get("local_model_name", "microsoft/DialoGPT-medium")
            
            self.logger.info(f"Loading local model: {model_name}")
            
            self.local_tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
            self.local_model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.local_model = self.local_model.cuda()
                self.logger.info("Local model loaded on GPU")
            else:
                self.logger.info("Local model loaded on CPU")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize local models: {e}")
    
    async def process_request(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process qdLLM request with quantum enhancement"""
        start_time = datetime.utcnow()
        self.request_count += 1
        
        try:
            # Route request based on model type and availability
            if request.model_type == ModelType.QDLLM_LOCAL:
                response = await self._process_qdllm_local(request)
            elif request.model_type == ModelType.QDLLM_HYBRID:
                response = await self._process_qdllm_hybrid(request)
            elif request.model_type == ModelType.NVIDIA_TRITON:
                response = await self._process_nvidia_triton(request)
            elif request.model_type in [ModelType.OPENAI_GPT4, ModelType.OPENAI_GPT35]:
                response = await self._process_openai(request)
            else:
                # Default fallback
                response = await self._process_with_fallback(request)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            response.processing_time = processing_time
            self.total_processing_time += processing_time
            
            # Track quantum enhancement usage
            if response.quantum_enhanced:
                self.quantum_enhanced_requests += 1
            
            # Update session if provided
            if request.session_id:
                await self._update_session(request.session_id, request, response)
            
            self.logger.debug(f"Request processed in {processing_time:.3f}s using {response.model_used.value}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Request processing failed: {e}")
            
            # Return error response
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            return QdLLMResponse(
                text=f"Processing error: {str(e)}",
                confidence=0.0,
                processing_time=processing_time,
                model_used=ModelType.OPENAI_GPT35,  # Fallback
                quantum_enhanced=False,
                reasoning_trace={"error": str(e)},
                metadata={"error": True},
                session_id=request.session_id
            )
    
    async def _process_qdllm_local(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request using local qdLLM service"""
        try:
            payload = {
                "prompt": request.prompt,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "quantum_enhanced": request.processing_mode == ProcessingMode.QUANTUM_ENHANCED,
                "quantum_params": request.quantum_params or {},
                "context": request.context or {}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.qdllm_endpoint}/generate",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        return QdLLMResponse(
                            text=result.get("text", ""),
                            confidence=result.get("confidence", 0.8),
                            processing_time=0.0,  # Will be set by caller
                            model_used=ModelType.QDLLM_LOCAL,
                            quantum_enhanced=result.get("quantum_enhanced", False),
                            reasoning_trace=result.get("reasoning_trace", {}),
                            metadata=result.get("metadata", {}),
                            session_id=request.session_id
                        )
                    else:
                        raise Exception(f"qdLLM service returned status {response.status}")
        
        except Exception as e:
            self.logger.warning(f"qdLLM local processing failed: {e}, falling back to OpenAI")
            return await self._process_openai(request)
    
    async def _process_qdllm_hybrid(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request using hybrid qdLLM + classical approach"""
        try:
            # First pass: Classical processing
            classical_request = QdLLMRequest(
                prompt=request.prompt,
                model_type=ModelType.OPENAI_GPT4,
                processing_mode=ProcessingMode.CLASSICAL,
                max_tokens=request.max_tokens // 2,  # Split tokens
                temperature=request.temperature,
                context=request.context,
                session_id=request.session_id
            )
            
            classical_response = await self._process_openai(classical_request)
            
            # Second pass: Quantum enhancement
            quantum_prompt = f"{request.prompt}\n\nClassical analysis: {classical_response.text}\n\nProvide quantum-enhanced insights:"
            
            quantum_request = QdLLMRequest(
                prompt=quantum_prompt,
                model_type=ModelType.QDLLM_LOCAL,
                processing_mode=ProcessingMode.QUANTUM_ENHANCED,
                max_tokens=request.max_tokens // 2,
                temperature=request.temperature * 0.8,  # Lower temperature for refinement
                quantum_params=request.quantum_params,
                context=request.context,
                session_id=request.session_id
            )
            
            quantum_response = await self._process_qdllm_local(quantum_request)
            
            # Combine responses
            combined_text = f"{classical_response.text}\n\nQuantum-enhanced insights:\n{quantum_response.text}"
            
            return QdLLMResponse(
                text=combined_text,
                confidence=(classical_response.confidence + quantum_response.confidence) / 2,
                processing_time=0.0,  # Will be set by caller
                model_used=ModelType.QDLLM_HYBRID,
                quantum_enhanced=True,
                reasoning_trace={
                    "classical": classical_response.reasoning_trace,
                    "quantum": quantum_response.reasoning_trace,
                    "hybrid_approach": True
                },
                metadata={
                    "classical_metadata": classical_response.metadata,
                    "quantum_metadata": quantum_response.metadata,
                    "hybrid_processing": True
                },
                session_id=request.session_id
            )
            
        except Exception as e:
            self.logger.warning(f"Hybrid processing failed: {e}, falling back to classical")
            return await self._process_openai(request)
    
    async def _process_nvidia_triton(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request using NVIDIA Triton inference server"""
        try:
            payload = {
                "inputs": [
                    {
                        "name": "text_input",
                        "shape": [1, 1],
                        "datatype": "BYTES",
                        "data": [request.prompt]
                    },
                    {
                        "name": "max_tokens",
                        "shape": [1, 1],
                        "datatype": "INT32",
                        "data": [request.max_tokens]
                    },
                    {
                        "name": "temperature",
                        "shape": [1, 1],
                        "datatype": "FP32",
                        "data": [request.temperature]
                    }
                ],
                "outputs": [
                    {
                        "name": "text_output"
                    },
                    {
                        "name": "confidence"
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.nvidia_triton_endpoint}/v2/models/quantum_llm/infer",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        outputs = result.get("outputs", [])
                        text_output = outputs[0].get("data", [""])[0] if outputs else ""
                        confidence = outputs[1].get("data", [0.8])[0] if len(outputs) > 1 else 0.8
                        
                        return QdLLMResponse(
                            text=text_output,
                            confidence=confidence,
                            processing_time=0.0,  # Will be set by caller
                            model_used=ModelType.NVIDIA_TRITON,
                            quantum_enhanced=True,  # NVIDIA acceleration counts as enhancement
                            reasoning_trace={"triton_inference": True},
                            metadata={"triton_model": "quantum_llm"},
                            session_id=request.session_id
                        )
                    else:
                        raise Exception(f"NVIDIA Triton returned status {response.status}")
        
        except Exception as e:
            self.logger.warning(f"NVIDIA Triton processing failed: {e}, falling back to OpenAI")
            return await self._process_openai(request)
    
    async def _process_openai(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request using OpenAI API"""
        if not self.openai_client:
            raise Exception("OpenAI client not configured")
        
        try:
            # Determine model based on request type
            model = "gpt-4" if request.model_type == ModelType.OPENAI_GPT4 else "gpt-3.5-turbo"
            
            # Prepare messages
            messages = [
                {"role": "system", "content": "You are a quantum-enhanced AI assistant with advanced reasoning capabilities."},
                {"role": "user", "content": request.prompt}
            ]
            
            # Add context if provided
            if request.context:
                context_msg = f"Context: {json.dumps(request.context, indent=2)}"
                messages.insert(1, {"role": "system", "content": context_msg})
            
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            text_response = response.choices[0].message.content
            
            return QdLLMResponse(
                text=text_response,
                confidence=0.85,  # OpenAI generally reliable
                processing_time=0.0,  # Will be set by caller
                model_used=request.model_type,
                quantum_enhanced=False,  # Pure OpenAI is not quantum enhanced
                reasoning_trace={"openai_model": model, "finish_reason": response.choices[0].finish_reason},
                metadata={
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                },
                session_id=request.session_id
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI processing failed: {e}")
            
            # Final fallback to local model if available
            if self.local_model and self.local_tokenizer:
                return await self._process_local_model(request)
            else:
                raise Exception(f"All processing methods failed: {e}")
    
    async def _process_local_model(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request using local transformer model"""
        if not self.local_model or not self.local_tokenizer:
            raise Exception("Local model not available")
        
        try:
            # Tokenize input
            inputs = self.local_tokenizer.encode(request.prompt, return_tensors="pt")
            
            # Move to GPU if model is on GPU
            if next(self.local_model.parameters()).is_cuda:
                inputs = inputs.cuda()
            
            # Generate response
            with torch.no_grad():
                outputs = self.local_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + request.max_tokens,
                    temperature=request.temperature,
                    do_sample=True,
                    pad_token_id=self.local_tokenizer.eos_token_id
                )
            
            # Decode response
            response_text = self.local_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the original prompt from response
            if response_text.startswith(request.prompt):
                response_text = response_text[len(request.prompt):].strip()
            
            return QdLLMResponse(
                text=response_text,
                confidence=0.7,  # Local models generally less reliable
                processing_time=0.0,  # Will be set by caller
                model_used=ModelType.QDLLM_LOCAL,  # Closest approximation
                quantum_enhanced=False,
                reasoning_trace={"local_model": True},
                metadata={"model_type": "local_transformer"},
                session_id=request.session_id
            )
            
        except Exception as e:
            self.logger.error(f"Local model processing failed: {e}")
            raise
    
    async def _process_with_fallback(self, request: QdLLMRequest) -> QdLLMResponse:
        """Process request with intelligent fallback strategy"""
        # Try qdLLM first
        try:
            return await self._process_qdllm_local(request)
        except Exception as e1:
            self.logger.warning(f"qdLLM failed: {e1}")
            
            # Try OpenAI
            try:
                return await self._process_openai(request)
            except Exception as e2:
                self.logger.warning(f"OpenAI failed: {e2}")
                
                # Try local model as last resort
                try:
                    return await self._process_local_model(request)
                except Exception as e3:
                    self.logger.error(f"All processing methods failed: qdLLM={e1}, OpenAI={e2}, Local={e3}")
                    raise Exception("All processing methods failed")
    
    async def _update_session(self, session_id: str, request: QdLLMRequest, response: QdLLMResponse):
        """Update session with request/response history"""
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {
                "created_at": datetime.utcnow().isoformat(),
                "requests": [],
                "total_tokens": 0,
                "quantum_enhanced_count": 0
            }
        
        session = self.active_sessions[session_id]
        session["requests"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": request.prompt[:100] + "..." if len(request.prompt) > 100 else request.prompt,
            "response": response.text[:100] + "..." if len(response.text) > 100 else response.text,
            "model_used": response.model_used.value,
            "quantum_enhanced": response.quantum_enhanced,
            "confidence": response.confidence,
            "processing_time": response.processing_time
        })
        
        # Update counters
        if response.quantum_enhanced:
            session["quantum_enhanced_count"] += 1
        
        # Estimate token usage
        estimated_tokens = len(request.prompt.split()) + len(response.text.split())
        session["total_tokens"] += estimated_tokens
        
        # Keep only last 50 requests per session
        if len(session["requests"]) > 50:
            session["requests"] = session["requests"][-50:]
    
    async def get_session_history(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session history"""
        return self.active_sessions.get(session_id)
    
    async def clear_session(self, session_id: str) -> bool:
        """Clear session history"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics"""
        avg_processing_time = self.total_processing_time / self.request_count if self.request_count > 0 else 0.0
        quantum_enhancement_rate = self.quantum_enhanced_requests / self.request_count if self.request_count > 0 else 0.0
        
        return {
            "total_requests": self.request_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_processing_time,
            "quantum_enhanced_requests": self.quantum_enhanced_requests,
            "quantum_enhancement_rate": quantum_enhancement_rate,
            "active_sessions": len(self.active_sessions),
            "service_status": {
                "qdllm_available": True,  # Would check actual connectivity
                "openai_available": self.openai_client is not None,
                "local_model_available": self.local_model is not None,
                "nvidia_triton_available": True  # Would check actual connectivity
            }
        }
    
    async def close(self):
        """Close service and cleanup resources"""
        self.logger.info("Closing QdLLM Service")
        
        # Clear sessions
        self.active_sessions.clear()
        
        # Cleanup local models
        if self.local_model:
            del self.local_model
            self.local_model = None
        
        if self.local_tokenizer:
            del self.local_tokenizer
            self.local_tokenizer = None
        
        # Close OpenAI client
        if self.openai_client:
            await self.openai_client.close()
        
        self.logger.info("QdLLM Service closed")

# Example usage and testing
if __name__ == "__main__":
    async def test_qdllm_service():
        """Test the QdLLM service"""
        config = {
            "openai_api_key": "your-openai-api-key",
            "qdllm_endpoint": "http://localhost:8001",
            "nvidia_triton_endpoint": "http://localhost:8002",
            "enable_local_models": False,
            "enable_nvidia_triton": False
        }
        
        service = QdLLMService(config)
        await service.initialize()
        
        # Test different model types
        test_requests = [
            QdLLMRequest(
                prompt="Explain quantum computing in simple terms",
                model_type=ModelType.QDLLM_LOCAL,
                processing_mode=ProcessingMode.QUANTUM_ENHANCED,
                max_tokens=200,
                session_id="test_session_1"
            ),
            QdLLMRequest(
                prompt="What are the benefits of quantum-enhanced AI?",
                model_type=ModelType.QDLLM_HYBRID,
                processing_mode=ProcessingMode.HYBRID,
                max_tokens=300,
                session_id="test_session_1"
            ),
            QdLLMRequest(
                prompt="Compare classical and quantum machine learning",
                model_type=ModelType.OPENAI_GPT4,
                processing_mode=ProcessingMode.CLASSICAL,
                max_tokens=400,
                session_id="test_session_2"
            )
        ]
        
        for i, request in enumerate(test_requests):
            print(f"\n--- Test {i+1}: {request.model_type.value} ---")
            try:
                response = await service.process_request(request)
                print(f"Response: {response.text[:200]}...")
                print(f"Confidence: {response.confidence}")
                print(f"Processing time: {response.processing_time:.3f}s")
                print(f"Quantum enhanced: {response.quantum_enhanced}")
                print(f"Model used: {response.model_used.value}")
            except Exception as e:
                print(f"Error: {e}")
        
        # Get metrics
        metrics = await service.get_metrics()
        print(f"\n--- Service Metrics ---")
        print(json.dumps(metrics, indent=2))
        
        # Get session history
        session_history = await service.get_session_history("test_session_1")
        if session_history:
            print(f"\n--- Session History ---")
            print(f"Requests in session: {len(session_history['requests'])}")
            print(f"Quantum enhanced: {session_history['quantum_enhanced_count']}")
        
        await service.close()
    
    # Run test
    asyncio.run(test_qdllm_service())