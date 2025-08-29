try:
    from src.branding import BRANDING
except ImportError:
    BRANDING = {
        'goliath': {'name': 'Goliath of All Trade'},
        'flyfox': {'name': 'Fly Fox AI'},
        'sigma_select': {'name': 'Sigma Select'}
    }
"""Logging Management Utility"""

import logging
import sys
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
from datetime import datetime
from utils.config import get_config

class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        structured = {
            'brand': f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}",
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        if hasattr(record, 'extra_fields'):
            structured.update(record.extra_fields)
        if record.exc_info:
            structured['exception'] = self.formatException(record.exc_info)
        return json.dumps(structured, ensure_ascii=False)

class ColoredFormatter(logging.Formatter):
    """Colored console formatter"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        formatted = super().format(record)
        return f"{color}{formatted}{reset}"

class Logger:
    """Enhanced logger with structured logging and configuration support"""
    
    def __init__(self, name: str = None, config: Optional[Dict] = None):
        """Initialize logger"""
        self.name = name or __name__
        self.config = config or get_config().logging
        self.logger = logging.getLogger(self.name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with handlers and formatters"""
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Set log level
        level = getattr(logging, self.config.level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # Console handler
        if self.config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            
            # Use colored formatter for console
            console_formatter = ColoredFormatter(
                fmt=self.config.format,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if self.config.file_path:
            try:
                file_path = Path(self.config.file_path)
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(file_path, encoding='utf-8')
                file_handler.setLevel(level)
                
                # Use structured formatter for file
                file_formatter = StructuredFormatter()
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Could not setup file logging: {e}")
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def _log_with_extra(self, level: int, message: str, **kwargs):
        """Log message with extra fields"""
        extra_fields = {k: v for k, v in kwargs.items() if not k.startswith('_')}
        
        if extra_fields:
            # Create a custom record with extra fields
            record = self.logger.makeRecord(
                self.name, level, "", 0, message, (), None
            )
            record.extra_fields = extra_fields
            self.logger.handle(record)
        else:
            self.logger.log(level, message)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self._log_with_extra(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self._log_with_extra(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self._log_with_extra(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self._log_with_extra(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self._log_with_extra(logging.CRITICAL, message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception message with traceback"""
        self._log_with_extra(logging.ERROR, message, exc_info=True, **kwargs)
    
    def log_quantum_execution(self, operation: str, qubits: int, backend: str, 
                            execution_time: float, success: bool, **kwargs):
        """Log quantum execution details"""
        self.info(
            f"Quantum execution: {operation}",
            operation=operation,
            qubits=qubits,
            backend=backend,
            execution_time=execution_time,
            success=success,
            **kwargs
        )
    
    def log_dynex_submission(self, problem_hash: str, solution_hash: str, 
                           credits_earned: float, **kwargs):
        """Log Dynex submission details"""
        self.info(
            f"Dynex submission completed",
            problem_hash=problem_hash,
            solution_hash=solution_hash,
            credits_earned=credits_earned,
            **kwargs
        )
    
    def log_agent_interaction(self, agent_type: str, user_input: str, 
                            response: str, processing_time: float, **kwargs):
        """Log AI agent interaction details"""
        self.info(
            f"Agent interaction: {agent_type}",
            agent_type=agent_type,
            user_input=user_input[:100] + "..." if len(user_input) > 100 else user_input,
            response=response[:100] + "..." if len(response) > 100 else response,
            processing_time=processing_time,
            **kwargs
        )

class LoggerFactory:
    """Factory for creating loggers with consistent configuration"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> Logger:
        """Get or create a logger instance"""
        if name not in cls._loggers:
            cls._loggers[name] = Logger(name)
        return cls._loggers[name]
    
    @classmethod
    def configure_all(cls, config: Dict):
        """Reconfigure all existing loggers"""
        for logger in cls._loggers.values():
            logger.config = config
            logger._setup_logger()

# Convenience functions
def get_logger(name: str = None) -> Logger:
    """Get a logger instance"""
    return LoggerFactory.get_logger(name or __name__)

def setup_logging(config: Dict):
    """Setup logging configuration for all loggers"""
    LoggerFactory.configure_all(config)

# Default logger instance
logger = get_logger(__name__) 
