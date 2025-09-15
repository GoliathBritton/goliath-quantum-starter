#!/usr/bin/env python3
"""
Database initialization script for the Goliath Quantum API.

This script handles:
- Database connection testing
- Running Alembic migrations
- Creating initial data
- Database health checks
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional

# Add the src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from database import (
    engine, async_engine, 
    check_database_health, check_database_health_async,
    init_database, init_database_async,
    get_pool_status
)
from models.base import Base
from models.partner import Partner
from models.user import User
from models.lead import Lead
from models.oracle_query import OracleQuery
from models.quantum_credit import QuantumCredit
from models.audit_log import AuditLog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_alembic_migrations():
    """Run Alembic migrations to set up database schema."""
    try:
        from alembic.config import Config
        from alembic import command
        
        # Get the alembic.ini path
        alembic_cfg_path = Path(__file__).parent.parent / "alembic.ini"
        
        if not alembic_cfg_path.exists():
            logger.error(f"Alembic config not found at {alembic_cfg_path}")
            return False
            
        # Create Alembic config
        alembic_cfg = Config(str(alembic_cfg_path))
        
        # Override database URL if needed
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            alembic_cfg.set_main_option("sqlalchemy.url", database_url)
        
        logger.info("Running Alembic migrations...")
        
        # Run migrations
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Alembic migrations completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to run Alembic migrations: {e}")
        return False

def create_initial_data():
    """Create initial data for development/testing."""
    try:
        from sqlalchemy.orm import sessionmaker
        from datetime import datetime, timedelta
        import uuid
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Check if data already exists
            existing_partner = db.query(Partner).first()
            if existing_partner:
                logger.info("Initial data already exists, skipping creation")
                return True
            
            logger.info("Creating initial data...")
            
            # Create demo partner
            demo_partner = Partner(
                id=str(uuid.uuid4()),
                name="Demo Partner",
                slug="demo-partner",
                email="demo@example.com",
                status="active",
                tier="starter",
                quantum_credits=1000,
                credits_used=0,
                rate_limit_per_minute=60,
                rate_limit_per_hour=1000,
                white_label_enabled=False,
                salesforce_enabled=False,
                hubspot_enabled=False,
                zapier_enabled=False,
                gdpr_compliant=True,
                ccpa_compliant=True,
                data_retention_days=365,
                onboarding_completed=True,
                trial_ends_at=datetime.utcnow() + timedelta(days=30)
            )
            db.add(demo_partner)
            db.flush()  # Get the ID
            
            # Create demo admin user
            demo_user = User(
                id=str(uuid.uuid4()),
                partner_id=demo_partner.id,
                email="admin@demo.com",
                first_name="Demo",
                last_name="Admin",
                is_active=True,
                is_verified=True,
                role="admin",
                language="en",
                theme="light",
                notifications_enabled=True,
                login_count=0,
                failed_login_attempts=0,
                totp_enabled=False,
                api_access_enabled=True,
                onboarding_completed=True,
                training_completed=False,
                marketing_consent=False,
                data_processing_consent=True
            )
            db.add(demo_user)
            db.flush()
            
            # Create demo lead
            demo_lead = Lead(
                id=str(uuid.uuid4()),
                partner_id=demo_partner.id,
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                company="Example Corp",
                title="CTO",
                status="new",
                stage="prospect",
                priority="medium",
                temperature="warm",
                page_views=0,
                email_opens=0,
                email_clicks=0,
                form_submissions=0,
                content_downloads=0,
                webinar_attendance=0,
                demo_requests=0,
                engagement_score=0,
                tcpa_consent=True,
                tcpa_consent_date=datetime.utcnow(),
                tcpa_consent_method="web_form",
                marketing_consent=True
            )
            db.add(demo_lead)
            
            # Commit all changes
            db.commit()
            logger.info("Initial data created successfully")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create initial data: {e}")
            return False
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Failed to set up initial data creation: {e}")
        return False

def test_database_connection() -> bool:
    """Test database connection and basic operations."""
    logger.info("Testing database connection...")
    
    # Test sync connection
    if not check_database_health():
        logger.error("Synchronous database connection failed")
        return False
    
    logger.info("Synchronous database connection successful")
    
    # Test async connection
    async def test_async():
        return await check_database_health_async()
    
    try:
        if not asyncio.run(test_async()):
            logger.error("Asynchronous database connection failed")
            return False
    except Exception as e:
        logger.error(f"Asynchronous database connection test failed: {e}")
        return False
    
    logger.info("Asynchronous database connection successful")
    
    # Show connection pool status
    pool_status = get_pool_status()
    logger.info(f"Connection pool status: {pool_status}")
    
    return True

def main():
    """Main initialization function."""
    logger.info("Starting database initialization...")
    
    # Test database connection first
    if not test_database_connection():
        logger.error("Database connection test failed. Please check your database configuration.")
        sys.exit(1)
    
    # Run migrations
    if not run_alembic_migrations():
        logger.error("Database migration failed")
        sys.exit(1)
    
    # Create initial data for development
    if os.getenv("CREATE_INITIAL_DATA", "false").lower() == "true":
        if not create_initial_data():
            logger.error("Failed to create initial data")
            sys.exit(1)
    
    logger.info("Database initialization completed successfully!")
    
    # Final health check
    if test_database_connection():
        logger.info("Final database health check passed")
    else:
        logger.warning("Final database health check failed")

if __name__ == "__main__":
    main()