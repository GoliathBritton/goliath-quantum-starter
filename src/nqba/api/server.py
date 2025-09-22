"""FastAPI Server - Main server application for qdLLM API

This module creates and configures the FastAPI application with all
routes, middleware, and services for the qdLLM platform.
"""

import os
import sys
import logging
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# Import API components
from .routes import api_router, initialize_services
from .middleware import setup_middleware
from .models import APIConfig, ErrorResponse
from .utils import ConfigManager, metrics_collector, response_cache

# Import core modules
from ..core.engine import qdLLMEngine
from ..qnlp.processor import QNLPProcessor
from ..qtransformers.model import QTransformerModel
from ..core.parallel_executor import ParallelExecutor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global configuration
config_manager: ConfigManager = None
app_config: Dict[str, Any] = {
    # Server settings
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "reload": False,
    
    # API settings
    "title": "qdLLM API",
    "description": "Quantum-enhanced Large Language Model API with QNLP and QTransformers",
    "version": "1.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json",
    
    # Model settings
    "default_model_type": "qdllm",
    "enable_quantum_enhancement": True,
    "model_cache_size": 1000,
    
    # Performance settings
    "max_concurrent_requests": 10,
    "request_timeout": 300.0,
    "worker_processes": 1,
    
    # Security settings
    "enable_cors": True,
    "cors_origins": ["*"],
    "api_key_required": False,
    "api_keys": {},
    "rate_limit_enabled": True,
    "rate_limit_per_minute": 60,
    "rate_limit_per_hour": 1000,
    
    # Logging settings
    "log_level": "INFO",
    "log_requests": True,
    "log_responses": False,
    
    # Cache settings
    "enable_caching": True,
    "cache_ttl": 3600,
    "cache_max_size": 1000,
    
    # Quantum settings
    "quantum_backend": "simulator",
    "quantum_shots": 1024,
    "quantum_optimization_level": 1,
    
    # Model initialization
    "initialize_models_on_startup": True,
    "model_warmup": True
}

# Service instances
qdllm_engine: qdLLMEngine = None
qnlp_processor: QNLPProcessor = None
qtransformer_model: QTransformerModel = None
parallel_executor: ParallelExecutor = None

async def initialize_models():
    """Initialize all models and services"""
    global qdllm_engine, qnlp_processor, qtransformer_model, parallel_executor
    
    try:
        logger.info("Initializing qdLLM services...")
        
        # Initialize parallel executor first
        logger.info("Initializing parallel executor...")
        parallel_executor = ParallelExecutor(
            max_workers=config_manager.get("max_concurrent_requests", 10),
            batch_size=config_manager.get("batch_size", 8)
        )
        
        # Initialize qdLLM engine
        logger.info("Initializing qdLLM engine...")
        engine_config = {
            "quantum_enhancement": config_manager.get("enable_quantum_enhancement", True),
            "quantum_backend": config_manager.get("quantum_backend", "simulator"),
            "quantum_shots": config_manager.get("quantum_shots", 1024),
            "cache_size": config_manager.get("model_cache_size", 1000),
            "parallel_executor": parallel_executor
        }
        qdllm_engine = qdLLMEngine(config=engine_config)
        
        # Initialize QNLP processor
        logger.info("Initializing QNLP processor...")
        qnlp_config = {
            "quantum_enhancement": config_manager.get("enable_quantum_enhancement", True),
            "embedding_dimension": config_manager.get("embedding_dimension", 256),
            "cache_size": config_manager.get("model_cache_size", 1000)
        }
        qnlp_processor = QNLPProcessor(config=qnlp_config)
        
        # Initialize QTransformer model
        logger.info("Initializing QTransformer model...")
        qtransformer_config = {
            "quantum_enhancement": config_manager.get("enable_quantum_enhancement", True),
            "model_size": config_manager.get("qtransformer_size", "base"),
            "num_layers": config_manager.get("qtransformer_layers", 6),
            "num_heads": config_manager.get("qtransformer_heads", 8)
        }
        qtransformer_model = QTransformerModel(config=qtransformer_config)
        
        # Initialize services in routes
        await initialize_services(
            qdllm_engine,
            qnlp_processor,
            qtransformer_model,
            parallel_executor
        )
        
        # Warm up models if enabled
        if config_manager.get("model_warmup", True):
            logger.info("Warming up models...")
            await warmup_models()
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise

async def warmup_models():
    """Warm up models with sample requests"""
    try:
        # Warm up qdLLM engine
        if qdllm_engine:
            await qdllm_engine.infer_async(
                prompt="Hello, world!",
                config={"max_length": 10, "temperature": 1.0}
            )
            logger.info("qdLLM engine warmed up")
        
        # Warm up QNLP processor
        if qnlp_processor:
            await qnlp_processor.process_async(
                text="Sample text for warmup",
                config={"analysis_depth": "basic"}
            )
            logger.info("QNLP processor warmed up")
        
        # Warm up QTransformer model
        if qtransformer_model:
            await qtransformer_model.generate_async(
                input_text="Sample input",
                config={"max_new_tokens": 5}
            )
            logger.info("QTransformer model warmed up")
        
    except Exception as e:
        logger.warning(f"Model warmup failed (non-critical): {str(e)}")

async def shutdown_models():
    """Shutdown all models and services"""
    global qdllm_engine, qnlp_processor, qtransformer_model, parallel_executor
    
    try:
        logger.info("Shutting down services...")
        
        # Shutdown services
        if parallel_executor:
            await parallel_executor.shutdown()
            logger.info("Parallel executor shut down")
        
        if qdllm_engine:
            await qdllm_engine.shutdown()
            logger.info("qdLLM engine shut down")
        
        if qnlp_processor:
            await qnlp_processor.shutdown()
            logger.info("QNLP processor shut down")
        
        if qtransformer_model:
            await qtransformer_model.shutdown()
            logger.info("QTransformer model shut down")
        
        # Clear caches
        response_cache.clear()
        logger.info("Caches cleared")
        
        logger.info("All services shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting qdLLM API server...")
    
    if config_manager.get("initialize_models_on_startup", True):
        await initialize_models()
    
    logger.info("qdLLM API server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down qdLLM API server...")
    await shutdown_models()
    logger.info("qdLLM API server shut down")

def create_app(config: Dict[str, Any] = None) -> FastAPI:
    """Create and configure FastAPI application"""
    global config_manager
    
    # Initialize configuration
    if config:
        app_config.update(config)
    config_manager = ConfigManager(app_config)
    
    # Configure logging
    log_level = config_manager.get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    # Create FastAPI app
    app = FastAPI(
        title=config_manager.get("title", "qdLLM API"),
        description=config_manager.get("description", "Quantum-enhanced Large Language Model API"),
        version=config_manager.get("version", "1.0.0"),
        docs_url=config_manager.get("docs_url", "/docs"),
        redoc_url=config_manager.get("redoc_url", "/redoc"),
        openapi_url=config_manager.get("openapi_url", "/openapi.json"),
        lifespan=lifespan
    )
    
    # Setup middleware
    setup_middleware(app, config_manager.to_dict())
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    # Custom exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": f"HTTP_{exc.status_code}",
                "error_message": exc.detail,
                "timestamp": metrics_collector.get_all_metrics()["timestamp"]
            }
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request, exc):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_code": "VALIDATION_ERROR",
                "error_message": str(exc),
                "timestamp": metrics_collector.get_all_metrics()["timestamp"]
            }
        )
    
    # Custom OpenAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        
        # Add custom schema information
        openapi_schema["info"]["x-logo"] = {
            "url": "https://example.com/logo.png"
        }
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key"
            },
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer"
            }
        }
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    # Additional endpoints
    @app.get("/", tags=["root"])
    async def root():
        """Root endpoint"""
        return {
            "name": app.title,
            "version": app.version,
            "description": app.description,
            "status": "running",
            "docs": "/docs",
            "api": "/api/v1",
            "health": "/api/v1/system/health"
        }
    
    @app.get("/metrics", tags=["monitoring"])
    async def get_app_metrics():
        """Get application metrics"""
        return {
            "app_metrics": metrics_collector.get_all_metrics(),
            "cache_stats": response_cache.get_stats(),
            "config": {
                "quantum_enhancement": config_manager.get("enable_quantum_enhancement"),
                "models_initialized": all([
                    qdllm_engine is not None,
                    qnlp_processor is not None,
                    qtransformer_model is not None
                ])
            }
        }
    
    return app

# Create the app instance
app = create_app()

# CLI functions
def load_config_from_file(config_path: str) -> Dict[str, Any]:
    """Load configuration from file"""
    import json
    import yaml
    
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith('.json'):
                return json.load(f)
            elif config_path.endswith(('.yml', '.yaml')):
                return yaml.safe_load(f)
            else:
                raise ValueError("Unsupported config file format")
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {str(e)}")
        return {}

def main():
    """Main entry point for running the server"""
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(description="qdLLM API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--log-level", default="INFO", help="Log level")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    
    args = parser.parse_args()
    
    # Load configuration from file if provided
    config = {}
    if args.config:
        config = load_config_from_file(args.config)
    
    # Override with command line arguments
    config.update({
        "host": args.host,
        "port": args.port,
        "reload": args.reload,
        "debug": args.debug,
        "log_level": args.log_level,
        "worker_processes": args.workers
    })
    
    # Create app with configuration
    global app
    app = create_app(config)
    
    # Run server
    logger.info(f"Starting qdLLM API server on {args.host}:{args.port}")
    
    uvicorn.run(
        "src.qdllm.api.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower(),
        workers=args.workers if not args.reload else 1,
        access_log=True
    )

if __name__ == "__main__":
    main()