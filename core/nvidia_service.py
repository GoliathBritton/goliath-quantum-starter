import asyncio
import logging
import json
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple, AsyncGenerator
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import base64
import io

try:
    import redis.asyncio as redis
except ImportError:
    print("Warning: Redis library not installed. Install with: pip install redis")
    redis = None

try:
    import torch
    import torchvision.transforms as transforms
except ImportError:
    print("Warning: PyTorch not installed. Install with: pip install torch torchvision")
    torch = None
    transforms = None

try:
    import cv2
except ImportError:
    print("Warning: OpenCV not installed. Install with: pip install opencv-python")
    cv2 = None

# Mock TensorRT for development
class MockTensorRT:
    """Mock TensorRT for development when NVIDIA libraries are not available"""
    
    class Logger:
        def __init__(self):
            pass
    
    class Builder:
        def __init__(self, logger):
            self.logger = logger
        
        def create_network(self):
            return MockTensorRT.NetworkDefinition()
        
        def create_builder_config(self):
            return MockTensorRT.BuilderConfig()
        
        def build_engine(self, network, config):
            return MockTensorRT.Engine()
    
    class NetworkDefinition:
        def __init__(self):
            pass
    
    class BuilderConfig:
        def __init__(self):
            pass
        
        def set_memory_pool_limit(self, pool_type, limit):
            pass
    
    class Engine:
        def __init__(self):
            pass
        
        def create_execution_context(self):
            return MockTensorRT.ExecutionContext()
    
    class ExecutionContext:
        def __init__(self):
            pass
        
        def execute_v2(self, bindings):
            return True

try:
    import tensorrt as trt
except ImportError:
    print("Warning: TensorRT not installed. Using mock implementation.")
    trt = MockTensorRT()

# Enums
class ModelType(Enum):
    TTS = "text_to_speech"
    STT = "speech_to_text"
    AVATAR = "digital_avatar"
    NLP = "natural_language"
    VISION = "computer_vision"
    EMBEDDING = "embedding"
    DIFFUSION = "diffusion"

class AccelerationType(Enum):
    TENSORRT = "tensorrt"
    CUDA = "cuda"
    TRITON = "triton"
    ONNX = "onnx"
    CPU = "cpu"

class InferenceMode(Enum):
    REALTIME = "realtime"
    BATCH = "batch"
    STREAMING = "streaming"
    ASYNC = "async"

class OptimizationLevel(Enum):
    NONE = "none"
    BASIC = "basic"
    AGGRESSIVE = "aggressive"
    ULTRA = "ultra"

@dataclass
class ModelConfig:
    """Model configuration for NVIDIA acceleration"""
    model_id: str
    model_type: ModelType
    model_path: str
    acceleration_type: AccelerationType
    optimization_level: OptimizationLevel
    max_batch_size: int = 1
    max_sequence_length: int = 512
    precision: str = "fp16"
    memory_limit_mb: int = 2048
    warmup_iterations: int = 10
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class InferenceRequest:
    """Inference request"""
    request_id: str
    model_id: str
    input_data: Union[str, bytes, np.ndarray, Dict[str, Any]]
    mode: InferenceMode
    parameters: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    priority: int = 5
    timeout_ms: int = 30000
    callback_url: Optional[str] = None

@dataclass
class InferenceResponse:
    """Inference response"""
    request_id: str
    model_id: str
    output_data: Union[str, bytes, np.ndarray, Dict[str, Any]]
    latency_ms: float
    throughput_tokens_per_sec: Optional[float] = None
    memory_usage_mb: Optional[float] = None
    gpu_utilization: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class AvatarFrame:
    """Avatar animation frame"""
    frame_id: str
    timestamp: float
    visemes: List[float]  # Facial animation parameters
    audio_chunk: Optional[bytes] = None
    video_frame: Optional[np.ndarray] = None
    emotions: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class StreamingSession:
    """Streaming session for real-time inference"""
    session_id: str
    model_id: str
    mode: InferenceMode
    created_at: str
    last_activity: str
    active: bool = True
    buffer_size: int = 1024
    latency_target_ms: int = 100
    quality_target: float = 0.8
    metadata: Optional[Dict[str, Any]] = None

class NVIDIAService:
    """NVIDIA Acceleration Service for AI/ML workloads"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Redis connection for caching and session management
        self.redis_client = None
        if redis and self.config.get("redis_url"):
            self.redis_client = redis.from_url(self.config["redis_url"])
        
        # Model registry
        self.models: Dict[str, ModelConfig] = {}
        self.engines: Dict[str, Any] = {}  # TensorRT engines
        self.contexts: Dict[str, Any] = {}  # Execution contexts
        
        # Streaming sessions
        self.streaming_sessions: Dict[str, StreamingSession] = {}
        
        # Performance metrics
        self.total_inferences = 0
        self.total_latency_ms = 0.0
        self.gpu_memory_usage = 0.0
        self.active_sessions = 0
        
        # Device information
        self.device_info = self._get_device_info()
        
        # Avatar animation cache
        self.avatar_cache: Dict[str, List[AvatarFrame]] = {}
        
        self.logger.info("NVIDIA Service initialized")
    
    async def initialize(self):
        """Initialize the NVIDIA service"""
        try:
            # Test Redis connectivity
            if self.redis_client:
                await self.redis_client.ping()
                self.logger.info("Redis connectivity confirmed")
            
            # Initialize CUDA if available
            await self._initialize_cuda()
            
            # Load default models
            await self._load_default_models()
            
            # Initialize TensorRT
            await self._initialize_tensorrt()
            
            self.logger.info("NVIDIA Service initialization complete")
            
        except Exception as e:
            self.logger.error(f"NVIDIA Service initialization failed: {e}")
            raise
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get NVIDIA device information"""
        device_info = {
            "cuda_available": False,
            "device_count": 0,
            "devices": []
        }
        
        if torch and torch.cuda.is_available():
            device_info["cuda_available"] = True
            device_info["device_count"] = torch.cuda.device_count()
            
            for i in range(torch.cuda.device_count()):
                device_props = torch.cuda.get_device_properties(i)
                device_info["devices"].append({
                    "id": i,
                    "name": device_props.name,
                    "memory_total": device_props.total_memory,
                    "memory_available": torch.cuda.get_device_properties(i).total_memory - torch.cuda.memory_allocated(i),
                    "compute_capability": f"{device_props.major}.{device_props.minor}"
                })
        
        return device_info
    
    async def _initialize_cuda(self):
        """Initialize CUDA environment"""
        if torch and torch.cuda.is_available():
            # Set device
            torch.cuda.set_device(0)
            
            # Clear cache
            torch.cuda.empty_cache()
            
            self.logger.info(f"CUDA initialized with {torch.cuda.device_count()} devices")
        else:
            self.logger.warning("CUDA not available, falling back to CPU")
    
    async def _load_default_models(self):
        """Load default model configurations"""
        # TTS Model
        self.models["tts_tacotron2"] = ModelConfig(
            model_id="tts_tacotron2",
            model_type=ModelType.TTS,
            model_path="models/tacotron2.onnx",
            acceleration_type=AccelerationType.TENSORRT,
            optimization_level=OptimizationLevel.AGGRESSIVE,
            max_batch_size=4,
            max_sequence_length=1024,
            precision="fp16",
            memory_limit_mb=1024
        )
        
        # STT Model
        self.models["stt_wav2vec2"] = ModelConfig(
            model_id="stt_wav2vec2",
            model_type=ModelType.STT,
            model_path="models/wav2vec2.onnx",
            acceleration_type=AccelerationType.TENSORRT,
            optimization_level=OptimizationLevel.BASIC,
            max_batch_size=2,
            max_sequence_length=16000,
            precision="fp16",
            memory_limit_mb=2048
        )
        
        # Avatar Model
        self.models["avatar_metahuman"] = ModelConfig(
            model_id="avatar_metahuman",
            model_type=ModelType.AVATAR,
            model_path="models/metahuman.onnx",
            acceleration_type=AccelerationType.TENSORRT,
            optimization_level=OptimizationLevel.ULTRA,
            max_batch_size=1,
            max_sequence_length=512,
            precision="fp16",
            memory_limit_mb=4096
        )
        
        # NLP Model
        self.models["nlp_bert"] = ModelConfig(
            model_id="nlp_bert",
            model_type=ModelType.NLP,
            model_path="models/bert.onnx",
            acceleration_type=AccelerationType.TENSORRT,
            optimization_level=OptimizationLevel.AGGRESSIVE,
            max_batch_size=8,
            max_sequence_length=512,
            precision="fp16",
            memory_limit_mb=1536
        )
        
        # Embedding Model
        self.models["embedding_sentence_transformer"] = ModelConfig(
            model_id="embedding_sentence_transformer",
            model_type=ModelType.EMBEDDING,
            model_path="models/sentence_transformer.onnx",
            acceleration_type=AccelerationType.TENSORRT,
            optimization_level=OptimizationLevel.BASIC,
            max_batch_size=16,
            max_sequence_length=256,
            precision="fp16",
            memory_limit_mb=512
        )
        
        self.logger.info(f"Loaded {len(self.models)} default model configurations")
    
    async def _initialize_tensorrt(self):
        """Initialize TensorRT engines"""
        try:
            # Create TensorRT logger
            trt_logger = trt.Logger()
            
            # Initialize engines for each model
            for model_id, config in self.models.items():
                if config.acceleration_type == AccelerationType.TENSORRT:
                    engine = await self._build_tensorrt_engine(config, trt_logger)
                    if engine:
                        self.engines[model_id] = engine
                        self.contexts[model_id] = engine.create_execution_context()
                        self.logger.info(f"TensorRT engine created for {model_id}")
            
            self.logger.info(f"TensorRT initialization complete with {len(self.engines)} engines")
            
        except Exception as e:
            self.logger.warning(f"TensorRT initialization failed: {e}")
    
    async def _build_tensorrt_engine(self, config: ModelConfig, trt_logger) -> Optional[Any]:
        """Build TensorRT engine from model"""
        try:
            # Create builder
            builder = trt.Builder(trt_logger)
            network = builder.create_network()
            builder_config = builder.create_builder_config()
            
            # Set memory limit
            builder_config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, config.memory_limit_mb * 1024 * 1024)
            
            # Set precision
            if config.precision == "fp16" and builder.platform_has_fast_fp16:
                builder_config.set_flag(trt.BuilderFlag.FP16)
            elif config.precision == "int8" and builder.platform_has_fast_int8:
                builder_config.set_flag(trt.BuilderFlag.INT8)
            
            # Build engine (mock implementation)
            engine = builder.build_engine(network, builder_config)
            
            return engine
            
        except Exception as e:
            self.logger.error(f"Failed to build TensorRT engine for {config.model_id}: {e}")
            return None
    
    async def register_model(self, config: ModelConfig) -> bool:
        """Register a new model"""
        try:
            self.models[config.model_id] = config
            
            # Build TensorRT engine if needed
            if config.acceleration_type == AccelerationType.TENSORRT:
                trt_logger = trt.Logger()
                engine = await self._build_tensorrt_engine(config, trt_logger)
                if engine:
                    self.engines[config.model_id] = engine
                    self.contexts[config.model_id] = engine.create_execution_context()
            
            self.logger.info(f"Model {config.model_id} registered successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register model {config.model_id}: {e}")
            return False
    
    async def inference(self, request: InferenceRequest) -> InferenceResponse:
        """Perform inference"""
        start_time = datetime.utcnow()
        self.total_inferences += 1
        
        try:
            # Validate model exists
            if request.model_id not in self.models:
                raise ValueError(f"Model {request.model_id} not found")
            
            config = self.models[request.model_id]
            
            # Route to appropriate inference method
            if config.model_type == ModelType.TTS:
                output_data = await self._tts_inference(request, config)
            elif config.model_type == ModelType.STT:
                output_data = await self._stt_inference(request, config)
            elif config.model_type == ModelType.AVATAR:
                output_data = await self._avatar_inference(request, config)
            elif config.model_type == ModelType.NLP:
                output_data = await self._nlp_inference(request, config)
            elif config.model_type == ModelType.EMBEDDING:
                output_data = await self._embedding_inference(request, config)
            else:
                output_data = await self._generic_inference(request, config)
            
            # Calculate metrics
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            self.total_latency_ms += latency_ms
            
            # Get GPU metrics
            gpu_utilization, memory_usage = await self._get_gpu_metrics()
            
            response = InferenceResponse(
                request_id=request.request_id,
                model_id=request.model_id,
                output_data=output_data,
                latency_ms=latency_ms,
                memory_usage_mb=memory_usage,
                gpu_utilization=gpu_utilization,
                metadata={
                    "model_type": config.model_type.value,
                    "acceleration_type": config.acceleration_type.value,
                    "precision": config.precision,
                    "inference_timestamp": end_time.isoformat()
                }
            )
            
            self.logger.debug(f"Inference completed for {request.request_id} in {latency_ms:.2f}ms")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Inference failed for {request.request_id}: {e}")
            
            return InferenceResponse(
                request_id=request.request_id,
                model_id=request.model_id,
                output_data=None,
                latency_ms=0.0,
                error=str(e)
            )
    
    async def _tts_inference(self, request: InferenceRequest, config: ModelConfig) -> bytes:
        """Text-to-Speech inference"""
        text = request.input_data
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Mock TTS processing
        # In production, this would use actual TensorRT engine
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Generate mock audio data
        sample_rate = 22050
        duration = len(text) * 0.1  # Rough estimate
        samples = int(sample_rate * duration)
        audio_data = np.random.randn(samples).astype(np.float32)
        
        # Convert to bytes
        audio_bytes = audio_data.tobytes()
        
        return audio_bytes
    
    async def _stt_inference(self, request: InferenceRequest, config: ModelConfig) -> str:
        """Speech-to-Text inference"""
        audio_data = request.input_data
        
        # Mock STT processing
        await asyncio.sleep(0.2)  # Simulate processing time
        
        # Generate mock transcription
        transcription = "This is a mock transcription of the audio input."
        
        return transcription
    
    async def _avatar_inference(self, request: InferenceRequest, config: ModelConfig) -> Dict[str, Any]:
        """Digital Avatar inference"""
        input_data = request.input_data
        
        # Mock avatar processing
        await asyncio.sleep(0.05)  # Simulate real-time processing
        
        # Generate mock visemes and animation data
        visemes = [0.1, 0.3, 0.7, 0.5, 0.2, 0.8, 0.4, 0.6]  # Facial animation parameters
        emotions = {
            "happiness": 0.7,
            "surprise": 0.2,
            "neutral": 0.1
        }
        
        # Generate mock video frame
        if cv2:
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        else:
            frame = None
        
        avatar_data = {
            "visemes": visemes,
            "emotions": emotions,
            "frame": frame.tolist() if frame is not None else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return avatar_data
    
    async def _nlp_inference(self, request: InferenceRequest, config: ModelConfig) -> Dict[str, Any]:
        """Natural Language Processing inference"""
        text = request.input_data
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Mock NLP processing
        await asyncio.sleep(0.1)
        
        # Generate mock NLP results
        nlp_results = {
            "tokens": text.split(),
            "sentiment": {
                "positive": 0.7,
                "negative": 0.2,
                "neutral": 0.1
            },
            "entities": [
                {"text": "example", "label": "MISC", "confidence": 0.9}
            ],
            "intent": {
                "classification": "question",
                "confidence": 0.85
            }
        }
        
        return nlp_results
    
    async def _embedding_inference(self, request: InferenceRequest, config: ModelConfig) -> List[float]:
        """Embedding inference"""
        text = request.input_data
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Mock embedding processing
        await asyncio.sleep(0.05)
        
        # Generate mock embedding vector
        embedding_dim = 768  # BERT-like embedding dimension
        embedding = np.random.randn(embedding_dim).astype(np.float32)
        
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.tolist()
    
    async def _generic_inference(self, request: InferenceRequest, config: ModelConfig) -> Any:
        """Generic inference for other model types"""
        # Mock generic processing
        await asyncio.sleep(0.1)
        
        return {"result": "Generic inference result", "input_processed": True}
    
    async def _get_gpu_metrics(self) -> Tuple[Optional[float], Optional[float]]:
        """Get GPU utilization and memory usage"""
        if torch and torch.cuda.is_available():
            try:
                # Get memory usage
                memory_allocated = torch.cuda.memory_allocated(0)
                memory_total = torch.cuda.get_device_properties(0).total_memory
                memory_usage_mb = memory_allocated / (1024 * 1024)
                
                # Mock GPU utilization (would use nvidia-ml-py in production)
                gpu_utilization = min(memory_allocated / memory_total * 100, 100.0)
                
                return gpu_utilization, memory_usage_mb
            except Exception as e:
                self.logger.warning(f"Failed to get GPU metrics: {e}")
        
        return None, None
    
    async def create_streaming_session(self, model_id: str, mode: InferenceMode, config: Optional[Dict[str, Any]] = None) -> StreamingSession:
        """Create streaming session for real-time inference"""
        session_id = str(uuid.uuid4())
        
        session = StreamingSession(
            session_id=session_id,
            model_id=model_id,
            mode=mode,
            created_at=datetime.utcnow().isoformat(),
            last_activity=datetime.utcnow().isoformat(),
            active=True,
            buffer_size=config.get("buffer_size", 1024) if config else 1024,
            latency_target_ms=config.get("latency_target_ms", 100) if config else 100,
            quality_target=config.get("quality_target", 0.8) if config else 0.8,
            metadata=config
        )
        
        self.streaming_sessions[session_id] = session
        self.active_sessions += 1
        
        self.logger.info(f"Streaming session {session_id} created for model {model_id}")
        
        return session
    
    async def stream_inference(self, session_id: str, input_data: Any) -> AsyncGenerator[InferenceResponse, None]:
        """Stream inference for real-time processing"""
        if session_id not in self.streaming_sessions:
            raise ValueError(f"Streaming session {session_id} not found")
        
        session = self.streaming_sessions[session_id]
        session.last_activity = datetime.utcnow().isoformat()
        
        # Create inference request
        request = InferenceRequest(
            request_id=str(uuid.uuid4()),
            model_id=session.model_id,
            input_data=input_data,
            mode=session.mode,
            session_id=session_id
        )
        
        # Perform streaming inference
        try:
            if session.model_id in self.models:
                config = self.models[session.model_id]
                
                # For avatar streaming, generate continuous frames
                if config.model_type == ModelType.AVATAR:
                    async for frame in self._stream_avatar_frames(request, config, session):
                        yield frame
                
                # For TTS streaming, generate audio chunks
                elif config.model_type == ModelType.TTS:
                    async for chunk in self._stream_tts_chunks(request, config, session):
                        yield chunk
                
                # For other types, use regular inference
                else:
                    response = await self.inference(request)
                    yield response
            
        except Exception as e:
            self.logger.error(f"Streaming inference failed for session {session_id}: {e}")
            
            error_response = InferenceResponse(
                request_id=request.request_id,
                model_id=session.model_id,
                output_data=None,
                latency_ms=0.0,
                error=str(e)
            )
            yield error_response
    
    async def _stream_avatar_frames(self, request: InferenceRequest, config: ModelConfig, session: StreamingSession) -> AsyncGenerator[InferenceResponse, None]:
        """Stream avatar animation frames"""
        frame_rate = 30  # 30 FPS
        frame_duration = 1.0 / frame_rate
        
        for i in range(60):  # Stream for 2 seconds
            start_time = datetime.utcnow()
            
            # Generate avatar frame
            avatar_data = await self._avatar_inference(request, config)
            
            # Create frame object
            frame = AvatarFrame(
                frame_id=f"{session.session_id}_{i}",
                timestamp=start_time.timestamp(),
                visemes=avatar_data["visemes"],
                emotions=avatar_data["emotions"],
                video_frame=np.array(avatar_data["frame"]) if avatar_data["frame"] else None
            )
            
            # Calculate latency
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            response = InferenceResponse(
                request_id=f"{request.request_id}_{i}",
                model_id=request.model_id,
                output_data=asdict(frame),
                latency_ms=latency_ms,
                metadata={"frame_number": i, "fps": frame_rate}
            )
            
            yield response
            
            # Maintain frame rate
            await asyncio.sleep(max(0, frame_duration - latency_ms / 1000))
    
    async def _stream_tts_chunks(self, request: InferenceRequest, config: ModelConfig, session: StreamingSession) -> AsyncGenerator[InferenceResponse, None]:
        """Stream TTS audio chunks"""
        text = request.input_data
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Split text into chunks for streaming
        words = text.split()
        chunk_size = 5  # Words per chunk
        
        for i in range(0, len(words), chunk_size):
            start_time = datetime.utcnow()
            
            chunk_text = " ".join(words[i:i + chunk_size])
            
            # Generate audio for chunk
            chunk_request = InferenceRequest(
                request_id=f"{request.request_id}_{i}",
                model_id=request.model_id,
                input_data=chunk_text,
                mode=request.mode
            )
            
            audio_data = await self._tts_inference(chunk_request, config)
            
            end_time = datetime.utcnow()
            latency_ms = (end_time - start_time).total_seconds() * 1000
            
            response = InferenceResponse(
                request_id=chunk_request.request_id,
                model_id=request.model_id,
                output_data=audio_data,
                latency_ms=latency_ms,
                metadata={"chunk_index": i // chunk_size, "chunk_text": chunk_text}
            )
            
            yield response
    
    async def close_streaming_session(self, session_id: str) -> bool:
        """Close streaming session"""
        if session_id in self.streaming_sessions:
            session = self.streaming_sessions[session_id]
            session.active = False
            del self.streaming_sessions[session_id]
            self.active_sessions -= 1
            
            self.logger.info(f"Streaming session {session_id} closed")
            return True
        
        return False
    
    async def optimize_model(self, model_id: str, optimization_level: OptimizationLevel) -> bool:
        """Optimize model for better performance"""
        if model_id not in self.models:
            return False
        
        try:
            config = self.models[model_id]
            config.optimization_level = optimization_level
            
            # Rebuild TensorRT engine with new optimization
            if config.acceleration_type == AccelerationType.TENSORRT:
                trt_logger = trt.Logger()
                engine = await self._build_tensorrt_engine(config, trt_logger)
                if engine:
                    # Replace existing engine
                    if model_id in self.engines:
                        del self.engines[model_id]
                        del self.contexts[model_id]
                    
                    self.engines[model_id] = engine
                    self.contexts[model_id] = engine.create_execution_context()
            
            self.logger.info(f"Model {model_id} optimized to {optimization_level.value} level")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to optimize model {model_id}: {e}")
            return False
    
    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get model information"""
        if model_id not in self.models:
            return None
        
        config = self.models[model_id]
        
        # Get engine info if available
        engine_info = {}
        if model_id in self.engines:
            engine_info = {
                "engine_loaded": True,
                "context_available": model_id in self.contexts
            }
        
        return {
            "config": asdict(config),
            "engine_info": engine_info,
            "performance_metrics": await self._get_model_metrics(model_id)
        }
    
    async def _get_model_metrics(self, model_id: str) -> Dict[str, Any]:
        """Get performance metrics for a model"""
        # Mock metrics - in production, this would track actual usage
        return {
            "total_inferences": self.total_inferences,
            "average_latency_ms": self.total_latency_ms / max(self.total_inferences, 1),
            "throughput_per_sec": 0.0,
            "memory_usage_mb": self.gpu_memory_usage,
            "error_rate": 0.0
        }
    
    async def get_service_metrics(self) -> Dict[str, Any]:
        """Get service performance metrics"""
        gpu_utilization, memory_usage = await self._get_gpu_metrics()
        
        return {
            "total_inferences": self.total_inferences,
            "average_latency_ms": self.total_latency_ms / max(self.total_inferences, 1),
            "active_sessions": self.active_sessions,
            "loaded_models": len(self.models),
            "tensorrt_engines": len(self.engines),
            "gpu_metrics": {
                "utilization_percent": gpu_utilization,
                "memory_usage_mb": memory_usage,
                "device_info": self.device_info
            },
            "service_status": {
                "redis_available": self.redis_client is not None,
                "cuda_available": self.device_info["cuda_available"],
                "tensorrt_available": len(self.engines) > 0
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {}
        }
        
        # Check CUDA availability
        health_status["checks"]["cuda"] = {
            "status": "pass" if self.device_info["cuda_available"] else "warn",
            "message": f"CUDA available: {self.device_info['cuda_available']}"
        }
        
        # Check Redis connectivity
        if self.redis_client:
            try:
                await self.redis_client.ping()
                health_status["checks"]["redis"] = {"status": "pass", "message": "Redis connected"}
            except Exception as e:
                health_status["checks"]["redis"] = {"status": "fail", "message": f"Redis error: {e}"}
                health_status["status"] = "degraded"
        
        # Check model availability
        health_status["checks"]["models"] = {
            "status": "pass" if len(self.models) > 0 else "warn",
            "message": f"{len(self.models)} models loaded"
        }
        
        # Check TensorRT engines
        health_status["checks"]["tensorrt"] = {
            "status": "pass" if len(self.engines) > 0 else "warn",
            "message": f"{len(self.engines)} TensorRT engines loaded"
        }
        
        return health_status
    
    async def close(self):
        """Close service and cleanup resources"""
        self.logger.info("Closing NVIDIA Service")
        
        # Close all streaming sessions
        for session_id in list(self.streaming_sessions.keys()):
            await self.close_streaming_session(session_id)
        
        # Clear CUDA cache
        if torch and torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Close Redis connection
        if self.redis_client:
            await self.redis_client.close()
        
        # Clear engines and contexts
        self.engines.clear()
        self.contexts.clear()
        self.models.clear()
        
        self.logger.info("NVIDIA Service closed")

# Example usage and testing
if __name__ == "__main__":
    async def test_nvidia_service():
        """Test the NVIDIA service"""
        config = {
            "redis_url": "redis://localhost:6379"
        }
        
        service = NVIDIAService(config)
        await service.initialize()
        
        # Test TTS inference
        print("\n--- TTS Inference Test ---")
        tts_request = InferenceRequest(
            request_id="tts_test_1",
            model_id="tts_tacotron2",
            input_data="Hello, this is a test of the text-to-speech system.",
            mode=InferenceMode.REALTIME
        )
        
        tts_response = await service.inference(tts_request)
        print(f"TTS Response: {tts_response.latency_ms:.2f}ms latency")
        print(f"Audio data size: {len(tts_response.output_data) if tts_response.output_data else 0} bytes")
        
        # Test Avatar inference
        print("\n--- Avatar Inference Test ---")
        avatar_request = InferenceRequest(
            request_id="avatar_test_1",
            model_id="avatar_metahuman",
            input_data="Generate facial animation for speaking",
            mode=InferenceMode.STREAMING
        )
        
        avatar_response = await service.inference(avatar_request)
        print(f"Avatar Response: {avatar_response.latency_ms:.2f}ms latency")
        print(f"Visemes: {avatar_response.output_data.get('visemes', []) if avatar_response.output_data else []}")
        
        # Test streaming session
        print("\n--- Streaming Session Test ---")
        session = await service.create_streaming_session(
            model_id="avatar_metahuman",
            mode=InferenceMode.STREAMING,
            config={"latency_target_ms": 50}
        )
        
        print(f"Created streaming session: {session.session_id}")
        
        # Stream a few frames
        frame_count = 0
        async for response in service.stream_inference(session.session_id, "Test streaming input"):
            frame_count += 1
            print(f"Frame {frame_count}: {response.latency_ms:.2f}ms latency")
            if frame_count >= 5:  # Limit to 5 frames for testing
                break
        
        await service.close_streaming_session(session.session_id)
        
        # Get service metrics
        metrics = await service.get_service_metrics()
        print(f"\n--- Service Metrics ---")
        print(json.dumps(metrics, indent=2))
        
        # Health check
        health = await service.health_check()
        print(f"\n--- Health Check ---")
        print(json.dumps(health, indent=2))
        
        await service.close()
    
    # Run test
    asyncio.run(test_nvidia_service())