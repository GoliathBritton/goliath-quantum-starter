import os
from datetime import timedelta
from typing import Dict, Any

class Config:
    """Base configuration class for Quantum Nexus Calling Agent."""
    
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quantum-nexus-calling-agent-secret-key-2024'
    DEBUG = False
    TESTING = False
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///calling_agent.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Redis Configuration (for Celery and caching)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Calling Configuration
    MAX_CONCURRENT_CALLS = int(os.environ.get('MAX_CONCURRENT_CALLS', '10'))
    CALL_TIMEOUT_SECONDS = int(os.environ.get('CALL_TIMEOUT_SECONDS', '30'))
    RETRY_ATTEMPTS = int(os.environ.get('RETRY_ATTEMPTS', '3'))
    RETRY_DELAY_MINUTES = int(os.environ.get('RETRY_DELAY_MINUTES', '15'))
    
    # Campaign Configuration
    DEFAULT_CAMPAIGN_HOURS = {
        'start': '09:00',
        'end': '17:00'
    }
    DEFAULT_CAMPAIGN_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    MAX_CALLS_PER_CONTACT = int(os.environ.get('MAX_CALLS_PER_CONTACT', '5'))
    
    # Contact Management
    MAX_CONTACTS_PER_IMPORT = int(os.environ.get('MAX_CONTACTS_PER_IMPORT', '10000'))
    CONTACT_DEDUPLICATION = True
    
    # Security Configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "1000 per hour"
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'txt'}
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'calling_agent.log')
    
    # API Configuration
    API_RATE_LIMIT = "100 per minute"
    API_KEY = os.environ.get('API_KEY')
    
    # WebSocket Configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
    
    # Monitoring Configuration
    ENABLE_METRICS = os.environ.get('ENABLE_METRICS', 'true').lower() == 'true'
    METRICS_PORT = int(os.environ.get('METRICS_PORT', '9090'))
    
    # Email Configuration (for notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Webhook Configuration
    WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
    WEBHOOK_TIMEOUT = int(os.environ.get('WEBHOOK_TIMEOUT', '30'))
    
    # Analytics Configuration
    ANALYTICS_RETENTION_DAYS = int(os.environ.get('ANALYTICS_RETENTION_DAYS', '90'))
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///calling_agent_dev.db'
    SESSION_COOKIE_SECURE = False
    
    # Development-specific settings
    MAX_CONCURRENT_CALLS = 2
    CALL_TIMEOUT_SECONDS = 15
    
    # Disable rate limiting in development
    RATELIMIT_ENABLED = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to console in development
        import logging
        from logging import StreamHandler
        
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # Testing-specific settings
    MAX_CONCURRENT_CALLS = 1
    CALL_TIMEOUT_SECONDS = 5
    RETRY_ATTEMPTS = 1
    
    # Disable external services in testing
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class ProductionConfig(Config):
    """Production configuration."""
    
    # Production database (PostgreSQL recommended)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/calling_agent_prod'
    
    # Enhanced security in production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to file in production
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/calling_agent.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Quantum Nexus Calling Agent startup')

class DockerConfig(ProductionConfig):
    """Docker-specific configuration."""
    
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Log to stdout when running in containers
        import logging
        from logging import StreamHandler
        
        handler = StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

# Calling Agent Specific Settings
CALLING_SETTINGS = {
    'voice_settings': {
        'voice': 'alice',
        'language': 'en-US',
        'speed': 1.0,
        'pitch': 0.0
    },
    'recording_settings': {
        'enabled': True,
        'format': 'mp3',
        'quality': 'standard'
    },
    'compliance': {
        'do_not_call_list_enabled': True,
        'consent_required': True,
        'recording_disclosure': True,
        'opt_out_keywords': ['stop', 'remove', 'unsubscribe', 'opt out']
    },
    'analytics': {
        'track_call_duration': True,
        'track_outcomes': True,
        'track_agent_performance': True,
        'export_formats': ['csv', 'xlsx', 'json']
    }
}

# Contact Import Settings
IMPORT_SETTINGS = {
    'csv_settings': {
        'delimiter': ',',
        'quotechar': '"',
        'encoding': 'utf-8',
        'skip_header': True
    },
    'field_mapping': {
        'required_fields': ['name', 'phone'],
        'optional_fields': ['email', 'company', 'notes', 'priority'],
        'auto_detect': True
    },
    'validation': {
        'phone_format': 'international',
        'email_validation': True,
        'duplicate_detection': True
    }
}

# Campaign Settings
CAMPAIGN_SETTINGS = {
    'scheduling': {
        'timezone': 'UTC',
        'business_hours_only': True,
        'respect_holidays': True,
        'max_daily_calls': 1000
    },
    'retry_logic': {
        'no_answer_retry': True,
        'busy_retry': True,
        'failed_retry': True,
        'retry_intervals': [15, 60, 240]  # minutes
    },
    'outcomes': {
        'success_outcomes': ['sale', 'appointment', 'interested'],
        'retry_outcomes': ['no_answer', 'busy', 'callback'],
        'final_outcomes': ['not_interested', 'do_not_call', 'invalid_number']
    }
}

def get_config(config_name=None):
    """Get configuration class by name."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])

def validate_config(app):
    """Validate critical configuration settings."""
    required_settings = [
        'SECRET_KEY',
        'SQLALCHEMY_DATABASE_URI'
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not app.config.get(setting):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required configuration: {', '.join(missing_settings)}")
    
    # Validate Twilio settings if calling is enabled
    if app.config.get('ENABLE_CALLING', True):
        twilio_settings = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']
        missing_twilio = [s for s in twilio_settings if not app.config.get(s)]
        if missing_twilio:
            app.logger.warning(f"Twilio settings missing: {', '.join(missing_twilio)}. Calling features will be disabled.")
            app.config['ENABLE_CALLING'] = False
    
    return True