#!/usr/bin/env python3
"""
Quantum Nexus Calling Agent - Main Application Entry Point

A sophisticated calling agent system with 2M+ contact capacity,
real-time monitoring, campaign management, and comprehensive analytics.
"""

import os
import sys
from flask import Flask
from flask_socketio import SocketIO
from config import get_config, validate_config
from web_interface import create_app

def create_application(config_name=None):
    """Create and configure the Flask application."""
    
    # Get configuration
    config_class = get_config(config_name)
    
    # Create Flask app
    app = create_app(config_class)
    
    # Validate configuration
    try:
        validate_config(app)
    except ValueError as e:
        app.logger.error(f"Configuration validation failed: {e}")
        sys.exit(1)
    
    return app

def main():
    """Main application entry point."""
    
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create application
    app = create_application(config_name)
    
    # Get SocketIO instance
    socketio = app.extensions.get('socketio')
    
    # Application info
    app.logger.info("="*60)
    app.logger.info("Quantum Nexus Calling Agent System")
    app.logger.info("="*60)
    app.logger.info(f"Environment: {config_name}")
    app.logger.info(f"Debug Mode: {app.debug}")
    app.logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
    app.logger.info(f"Max Concurrent Calls: {app.config['MAX_CONCURRENT_CALLS']}")
    app.logger.info("="*60)
    
    # Run application
    if socketio:
        # Run with SocketIO support
        socketio.run(
            app,
            host=os.environ.get('HOST', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=app.debug,
            use_reloader=app.debug,
            log_output=True
        )
    else:
        # Fallback to standard Flask
        app.run(
            host=os.environ.get('HOST', '0.0.0.0'),
            port=int(os.environ.get('PORT', 5000)),
            debug=app.debug,
            use_reloader=app.debug
        )

if __name__ == '__main__':
    main()