import os
from typing import AsyncGenerator
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from src.models.base import Base
import logging

logger = logging.getLogger(__name__)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
if "sqlite" in DATABASE_URL:
    ASYNC_DATABASE_URL = "sqlite+aiosqlite:///app.db"
else:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Test Database (SQLite in-memory for testing)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Database Engine Configuration
engine_kwargs = {
    "echo": os.getenv("DB_ECHO", "false").lower() == "true",
    "pool_pre_ping": True,
    "pool_recycle": 3600,  # Recycle connections every hour
}

# For SQLite (testing)
if "sqlite" in DATABASE_URL:
    engine_kwargs.update({
        "poolclass": StaticPool,
        "connect_args": {"check_same_thread": False}
    })

# For PostgreSQL (production)
else:
    engine_kwargs.update({
        "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
    })

# Create engines
engine = create_engine(DATABASE_URL, **engine_kwargs)
async_engine = create_async_engine(ASYNC_DATABASE_URL, **engine_kwargs)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Test engine and session (for testing)
test_engine = None
TestSessionLocal = None

def create_test_engine():
    """Create test database engine."""
    global test_engine, TestSessionLocal
    test_engine = create_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return test_engine

def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

async def create_tables_async():
    """Create all database tables asynchronously."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully (async)")
    except Exception as e:
        logger.error(f"Error creating database tables (async): {e}")
        raise

def drop_tables():
    """Drop all database tables."""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping database tables: {e}")
        raise

async def drop_tables_async():
    """Drop all database tables asynchronously."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully (async)")
    except Exception as e:
        logger.error(f"Error dropping database tables (async): {e}")
        raise

def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Async database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

def get_test_db() -> Session:
    """Dependency to get test database session."""
    if TestSessionLocal is None:
        create_test_engine()
        Base.metadata.create_all(bind=test_engine)
    
    db = TestSessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Test database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

# Database health check
def check_database_health() -> bool:
    """Check if database is healthy and accessible."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False

async def check_database_health_async() -> bool:
    """Check if database is healthy and accessible (async)."""
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Async database health check failed: {e}")
        return False

# Database connection events
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance and consistency."""
    if "sqlite" in DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log database connection checkout."""
    logger.debug("Database connection checked out")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Log database connection checkin."""
    logger.debug("Database connection checked in")

# Connection pool monitoring
def get_pool_status() -> dict:
    """Get database connection pool status."""
    pool = engine.pool
    if hasattr(pool, 'size'):
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid() if hasattr(pool, 'invalid') else 0
        }
    else:
        # For StaticPool or similar
        return {
            "size": 1,
            "checked_in": 1,
            "checked_out": 0,
            "overflow": 0,
            "invalid": 0
        }

# Database initialization
def init_database():
    """Initialize database with tables and basic data."""
    try:
        logger.info("Initializing database...")
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def init_database_async():
    """Initialize database with tables and basic data (async)."""
    try:
        logger.info("Initializing database (async)...")
        await create_tables_async()
        logger.info("Database initialized successfully (async)")
    except Exception as e:
        logger.error(f"Failed to initialize database (async): {e}")
        raise

# Cleanup
def close_database():
    """Close database connections."""
    try:
        engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")

async def close_database_async():
    """Close async database connections."""
    try:
        await async_engine.dispose()
        logger.info("Async database connections closed")
    except Exception as e:
        logger.error(f"Error closing async database connections: {e}")