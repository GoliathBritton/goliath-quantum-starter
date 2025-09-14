import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

@dataclass
class DynexConfig:
    """Configuration for Dynex quantum annealing backend."""
    mainnet: bool = True
    testnet_url: Optional[str] = None
    num_reads: int = 1000
    annealing_time: int = 20
    chain_strength: float = 1.0
    num_spin_reversal_transforms: int = 0
    description: str = "Quantum optimization via QNE"
    logging: bool = True
    
@dataclass
class ClassicalConfig:
    """Configuration for classical optimization backends."""
    max_iterations: int = 1000
    convergence_threshold: float = 1e-6
    timeout_seconds: int = 300
    simulated_annealing: Dict[str, Any] = field(default_factory=lambda: {
        'initial_temperature': 1.0,
        'final_temperature': 0.01,
        'cooling_rate': 0.95
    })
    tabu_search: Dict[str, Any] = field(default_factory=lambda: {
        'tabu_tenure': 10,
        'max_iterations': 1000,
        'diversification_frequency': 100
    })
    genetic_algorithm: Dict[str, Any] = field(default_factory=lambda: {
        'population_size': 100,
        'mutation_rate': 0.1,
        'crossover_rate': 0.8,
        'elitism_rate': 0.1
    })

@dataclass
class HybridConfig:
    """Configuration for hybrid quantum-classical approaches."""
    max_subproblem_size: int = 50
    decomposition_strategy: str = "graph_partitioning"  # or "variable_clustering"
    quantum_threshold: int = 30  # Use quantum for subproblems <= this size
    local_optimization: bool = True
    max_local_iterations: int = 100
    
@dataclass
class ProblemConfig:
    """Configuration for specific problem types."""
    portfolio_optimization: Dict[str, Any] = field(default_factory=lambda: {
        'default_risk_aversion': 1.0,
        'budget_penalty_weight': 10.0,
        'min_assets_penalty_weight': 5.0,
        'max_assets_penalty_weight': 5.0
    })
    tsp: Dict[str, Any] = field(default_factory=lambda: {
        'constraint_penalty_multiplier': 100,
        'start_city_penalty': 1000
    })
    max_cut: Dict[str, Any] = field(default_factory=lambda: {
        'edge_weight_scaling': 1.0
    })
    job_scheduling: Dict[str, Any] = field(default_factory=lambda: {
        'assignment_penalty': 1000,
        'capacity_penalty': 500,
        'deadline_penalty_multiplier': 100
    })
    knapsack: Dict[str, Any] = field(default_factory=lambda: {
        'capacity_penalty_multiplier': 10
    })
    graph_coloring: Dict[str, Any] = field(default_factory=lambda: {
        'node_color_penalty': 100,
        'adjacent_color_penalty': 200,
        'color_usage_penalty': 1
    })

@dataclass
class PerformanceConfig:
    """Configuration for performance monitoring and optimization."""
    enable_profiling: bool = False
    memory_limit_mb: int = 4096
    cpu_timeout_seconds: int = 600
    max_concurrent_jobs: int = 10
    result_cache_size: int = 1000
    enable_result_caching: bool = True
    
@dataclass
class LoggingConfig:
    """Configuration for logging."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size_mb: int = 100
    backup_count: int = 5
    enable_console: bool = True
    
@dataclass
class SecurityConfig:
    """Configuration for security settings."""
    enable_input_validation: bool = True
    max_problem_size: int = 10000
    allowed_problem_types: list = field(default_factory=lambda: [
        'portfolio_optimization',
        'tsp',
        'max_cut',
        'job_scheduling',
        'knapsack',
        'graph_coloring',
        'custom'
    ])
    rate_limit_per_minute: int = 60
    enable_result_encryption: bool = False
    
class QuantumWorkerConfig:
    """Main configuration class for the Quantum Worker service."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        self.logger = logging.getLogger(__name__)
        
        # Load configuration from environment variables and config dict
        self._load_config(config_dict or {})
        
    def _load_config(self, config_dict: Dict[str, Any]):
        """Load configuration from environment variables and config dictionary."""
        
        # Dynex configuration
        dynex_config = config_dict.get('dynex', {})
        self.dynex = DynexConfig(
            mainnet=self._get_bool_env('DYNEX_MAINNET', dynex_config.get('mainnet', True)),
            testnet_url=self._get_env('DYNEX_TESTNET_URL', dynex_config.get('testnet_url')),
            num_reads=self._get_int_env('DYNEX_NUM_READS', dynex_config.get('num_reads', 1000)),
            annealing_time=self._get_int_env('DYNEX_ANNEALING_TIME', dynex_config.get('annealing_time', 20)),
            chain_strength=self._get_float_env('DYNEX_CHAIN_STRENGTH', dynex_config.get('chain_strength', 1.0)),
            num_spin_reversal_transforms=self._get_int_env('DYNEX_SPIN_REVERSAL', dynex_config.get('num_spin_reversal_transforms', 0)),
            description=self._get_env('DYNEX_DESCRIPTION', dynex_config.get('description', 'Quantum optimization via QNE')),
            logging=self._get_bool_env('DYNEX_LOGGING', dynex_config.get('logging', True))
        )
        
        # Classical configuration
        classical_config = config_dict.get('classical', {})
        self.classical = ClassicalConfig(
            max_iterations=self._get_int_env('CLASSICAL_MAX_ITERATIONS', classical_config.get('max_iterations', 1000)),
            convergence_threshold=self._get_float_env('CLASSICAL_CONVERGENCE_THRESHOLD', classical_config.get('convergence_threshold', 1e-6)),
            timeout_seconds=self._get_int_env('CLASSICAL_TIMEOUT', classical_config.get('timeout_seconds', 300)),
            simulated_annealing=classical_config.get('simulated_annealing', {
                'initial_temperature': 1.0,
                'final_temperature': 0.01,
                'cooling_rate': 0.95
            }),
            tabu_search=classical_config.get('tabu_search', {
                'tabu_tenure': 10,
                'max_iterations': 1000,
                'diversification_frequency': 100
            }),
            genetic_algorithm=classical_config.get('genetic_algorithm', {
                'population_size': 100,
                'mutation_rate': 0.1,
                'crossover_rate': 0.8,
                'elitism_rate': 0.1
            })
        )
        
        # Hybrid configuration
        hybrid_config = config_dict.get('hybrid', {})
        self.hybrid = HybridConfig(
            max_subproblem_size=self._get_int_env('HYBRID_MAX_SUBPROBLEM_SIZE', hybrid_config.get('max_subproblem_size', 50)),
            decomposition_strategy=self._get_env('HYBRID_DECOMPOSITION_STRATEGY', hybrid_config.get('decomposition_strategy', 'graph_partitioning')),
            quantum_threshold=self._get_int_env('HYBRID_QUANTUM_THRESHOLD', hybrid_config.get('quantum_threshold', 30)),
            local_optimization=self._get_bool_env('HYBRID_LOCAL_OPTIMIZATION', hybrid_config.get('local_optimization', True)),
            max_local_iterations=self._get_int_env('HYBRID_MAX_LOCAL_ITERATIONS', hybrid_config.get('max_local_iterations', 100))
        )
        
        # Problem-specific configuration
        self.problems = ProblemConfig(**config_dict.get('problems', {}))
        
        # Performance configuration
        performance_config = config_dict.get('performance', {})
        self.performance = PerformanceConfig(
            enable_profiling=self._get_bool_env('ENABLE_PROFILING', performance_config.get('enable_profiling', False)),
            memory_limit_mb=self._get_int_env('MEMORY_LIMIT_MB', performance_config.get('memory_limit_mb', 4096)),
            cpu_timeout_seconds=self._get_int_env('CPU_TIMEOUT_SECONDS', performance_config.get('cpu_timeout_seconds', 600)),
            max_concurrent_jobs=self._get_int_env('MAX_CONCURRENT_JOBS', performance_config.get('max_concurrent_jobs', 10)),
            result_cache_size=self._get_int_env('RESULT_CACHE_SIZE', performance_config.get('result_cache_size', 1000)),
            enable_result_caching=self._get_bool_env('ENABLE_RESULT_CACHING', performance_config.get('enable_result_caching', True))
        )
        
        # Logging configuration
        logging_config = config_dict.get('logging', {})
        self.logging = LoggingConfig(
            level=self._get_env('LOG_LEVEL', logging_config.get('level', 'INFO')),
            format=self._get_env('LOG_FORMAT', logging_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')),
            file_path=self._get_env('LOG_FILE_PATH', logging_config.get('file_path')),
            max_file_size_mb=self._get_int_env('LOG_MAX_FILE_SIZE_MB', logging_config.get('max_file_size_mb', 100)),
            backup_count=self._get_int_env('LOG_BACKUP_COUNT', logging_config.get('backup_count', 5)),
            enable_console=self._get_bool_env('LOG_ENABLE_CONSOLE', logging_config.get('enable_console', True))
        )
        
        # Security configuration
        security_config = config_dict.get('security', {})
        self.security = SecurityConfig(
            enable_input_validation=self._get_bool_env('ENABLE_INPUT_VALIDATION', security_config.get('enable_input_validation', True)),
            max_problem_size=self._get_int_env('MAX_PROBLEM_SIZE', security_config.get('max_problem_size', 10000)),
            allowed_problem_types=security_config.get('allowed_problem_types', [
                'portfolio_optimization', 'tsp', 'max_cut', 'job_scheduling', 'knapsack', 'graph_coloring', 'custom'
            ]),
            rate_limit_per_minute=self._get_int_env('RATE_LIMIT_PER_MINUTE', security_config.get('rate_limit_per_minute', 60)),
            enable_result_encryption=self._get_bool_env('ENABLE_RESULT_ENCRYPTION', security_config.get('enable_result_encryption', False))
        )
        
        self.logger.info("Quantum Worker configuration loaded successfully")
    
    def _get_env(self, key: str, default: Any = None) -> Any:
        """Get environment variable with default value."""
        return os.getenv(key, default)
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer environment variable with default value."""
        try:
            value = os.getenv(key)
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid integer value for {key}, using default: {default}")
            return default
    
    def _get_float_env(self, key: str, default: float) -> float:
        """Get float environment variable with default value."""
        try:
            value = os.getenv(key)
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid float value for {key}, using default: {default}")
            return default
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean environment variable with default value."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def get_backend_config(self, backend: str) -> Dict[str, Any]:
        """Get configuration for a specific backend."""
        if backend == 'dynex':
            return {
                'mainnet': self.dynex.mainnet,
                'testnet_url': self.dynex.testnet_url,
                'num_reads': self.dynex.num_reads,
                'annealing_time': self.dynex.annealing_time,
                'chain_strength': self.dynex.chain_strength,
                'num_spin_reversal_transforms': self.dynex.num_spin_reversal_transforms,
                'description': self.dynex.description,
                'logging': self.dynex.logging
            }
        elif backend == 'classical':
            return {
                'max_iterations': self.classical.max_iterations,
                'convergence_threshold': self.classical.convergence_threshold,
                'timeout_seconds': self.classical.timeout_seconds,
                'simulated_annealing': self.classical.simulated_annealing,
                'tabu_search': self.classical.tabu_search,
                'genetic_algorithm': self.classical.genetic_algorithm
            }
        elif backend == 'hybrid':
            return {
                'max_subproblem_size': self.hybrid.max_subproblem_size,
                'decomposition_strategy': self.hybrid.decomposition_strategy,
                'quantum_threshold': self.hybrid.quantum_threshold,
                'local_optimization': self.hybrid.local_optimization,
                'max_local_iterations': self.hybrid.max_local_iterations
            }
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def get_problem_config(self, problem_type: str) -> Dict[str, Any]:
        """Get configuration for a specific problem type."""
        problem_configs = {
            'portfolio_optimization': self.problems.portfolio_optimization,
            'tsp': self.problems.tsp,
            'max_cut': self.problems.max_cut,
            'job_scheduling': self.problems.job_scheduling,
            'knapsack': self.problems.knapsack,
            'graph_coloring': self.problems.graph_coloring
        }
        
        return problem_configs.get(problem_type, {})
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate the current configuration."""
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Validate Dynex configuration
        if self.dynex.num_reads <= 0:
            validation_result['errors'].append("Dynex num_reads must be positive")
            validation_result['valid'] = False
        
        if self.dynex.annealing_time <= 0:
            validation_result['errors'].append("Dynex annealing_time must be positive")
            validation_result['valid'] = False
        
        # Validate classical configuration
        if self.classical.max_iterations <= 0:
            validation_result['errors'].append("Classical max_iterations must be positive")
            validation_result['valid'] = False
        
        if self.classical.timeout_seconds <= 0:
            validation_result['errors'].append("Classical timeout_seconds must be positive")
            validation_result['valid'] = False
        
        # Validate hybrid configuration
        if self.hybrid.max_subproblem_size <= 0:
            validation_result['errors'].append("Hybrid max_subproblem_size must be positive")
            validation_result['valid'] = False
        
        if self.hybrid.quantum_threshold <= 0:
            validation_result['errors'].append("Hybrid quantum_threshold must be positive")
            validation_result['valid'] = False
        
        # Validate performance configuration
        if self.performance.memory_limit_mb <= 0:
            validation_result['errors'].append("Performance memory_limit_mb must be positive")
            validation_result['valid'] = False
        
        if self.performance.max_concurrent_jobs <= 0:
            validation_result['errors'].append("Performance max_concurrent_jobs must be positive")
            validation_result['valid'] = False
        
        # Validate security configuration
        if self.security.max_problem_size <= 0:
            validation_result['errors'].append("Security max_problem_size must be positive")
            validation_result['valid'] = False
        
        if self.security.rate_limit_per_minute <= 0:
            validation_result['errors'].append("Security rate_limit_per_minute must be positive")
            validation_result['valid'] = False
        
        # Add warnings for potentially problematic configurations
        if self.dynex.num_reads > 10000:
            validation_result['warnings'].append("High num_reads may result in long execution times")
        
        if self.classical.max_iterations > 10000:
            validation_result['warnings'].append("High max_iterations may result in long execution times")
        
        if self.performance.max_concurrent_jobs > 50:
            validation_result['warnings'].append("High max_concurrent_jobs may cause resource exhaustion")
        
        return validation_result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format."""
        return {
            'dynex': {
                'mainnet': self.dynex.mainnet,
                'testnet_url': self.dynex.testnet_url,
                'num_reads': self.dynex.num_reads,
                'annealing_time': self.dynex.annealing_time,
                'chain_strength': self.dynex.chain_strength,
                'num_spin_reversal_transforms': self.dynex.num_spin_reversal_transforms,
                'description': self.dynex.description,
                'logging': self.dynex.logging
            },
            'classical': {
                'max_iterations': self.classical.max_iterations,
                'convergence_threshold': self.classical.convergence_threshold,
                'timeout_seconds': self.classical.timeout_seconds,
                'simulated_annealing': self.classical.simulated_annealing,
                'tabu_search': self.classical.tabu_search,
                'genetic_algorithm': self.classical.genetic_algorithm
            },
            'hybrid': {
                'max_subproblem_size': self.hybrid.max_subproblem_size,
                'decomposition_strategy': self.hybrid.decomposition_strategy,
                'quantum_threshold': self.hybrid.quantum_threshold,
                'local_optimization': self.hybrid.local_optimization,
                'max_local_iterations': self.hybrid.max_local_iterations
            },
            'problems': {
                'portfolio_optimization': self.problems.portfolio_optimization,
                'tsp': self.problems.tsp,
                'max_cut': self.problems.max_cut,
                'job_scheduling': self.problems.job_scheduling,
                'knapsack': self.problems.knapsack,
                'graph_coloring': self.problems.graph_coloring
            },
            'performance': {
                'enable_profiling': self.performance.enable_profiling,
                'memory_limit_mb': self.performance.memory_limit_mb,
                'cpu_timeout_seconds': self.performance.cpu_timeout_seconds,
                'max_concurrent_jobs': self.performance.max_concurrent_jobs,
                'result_cache_size': self.performance.result_cache_size,
                'enable_result_caching': self.performance.enable_result_caching
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file_path': self.logging.file_path,
                'max_file_size_mb': self.logging.max_file_size_mb,
                'backup_count': self.logging.backup_count,
                'enable_console': self.logging.enable_console
            },
            'security': {
                'enable_input_validation': self.security.enable_input_validation,
                'max_problem_size': self.security.max_problem_size,
                'allowed_problem_types': self.security.allowed_problem_types,
                'rate_limit_per_minute': self.security.rate_limit_per_minute,
                'enable_result_encryption': self.security.enable_result_encryption
            }
        }
    
    def setup_logging(self):
        """Setup logging based on configuration."""
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.logging.level.upper()))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(self.logging.format)
        
        # Console handler
        if self.logging.enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler
        if self.logging.file_path:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                self.logging.file_path,
                maxBytes=self.logging.max_file_size_mb * 1024 * 1024,
                backupCount=self.logging.backup_count
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        self.logger.info("Logging configured successfully")

# Global configuration instance
_config_instance = None

def get_config(config_dict: Optional[Dict[str, Any]] = None) -> QuantumWorkerConfig:
    """Get the global configuration instance."""
    global _config_instance
    if _config_instance is None or config_dict is not None:
        _config_instance = QuantumWorkerConfig(config_dict)
    return _config_instance

def load_config_from_file(file_path: str) -> QuantumWorkerConfig:
    """Load configuration from a JSON or YAML file."""
    import json
    
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                config_dict = json.load(f)
            elif file_path.endswith(('.yaml', '.yml')):
                try:
                    import yaml
                    config_dict = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required to load YAML configuration files")
            else:
                raise ValueError("Configuration file must be JSON or YAML format")
        
        return QuantumWorkerConfig(config_dict)
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to load configuration from {file_path}: {e}")
        raise

# Default configuration for development
DEFAULT_CONFIG = {
    'dynex': {
        'mainnet': False,  # Use testnet for development
        'num_reads': 100,  # Reduced for faster development
        'annealing_time': 10
    },
    'classical': {
        'max_iterations': 500,
        'timeout_seconds': 60
    },
    'performance': {
        'max_concurrent_jobs': 5,
        'enable_result_caching': True
    },
    'logging': {
        'level': 'DEBUG',
        'enable_console': True
    },
    'security': {
        'max_problem_size': 1000,
        'rate_limit_per_minute': 30
    }
}

# Production configuration
PRODUCTION_CONFIG = {
    'dynex': {
        'mainnet': True,
        'num_reads': 1000,
        'annealing_time': 20
    },
    'classical': {
        'max_iterations': 2000,
        'timeout_seconds': 300
    },
    'performance': {
        'max_concurrent_jobs': 20,
        'enable_result_caching': True,
        'memory_limit_mb': 8192
    },
    'logging': {
        'level': 'INFO',
        'enable_console': True,
        'file_path': '/var/log/quantum-worker.log'
    },
    'security': {
        'max_problem_size': 10000,
        'rate_limit_per_minute': 100,
        'enable_input_validation': True
    }
}