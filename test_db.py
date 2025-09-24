import os

from sqlalchemy.ext.asyncio import create_async_engine

try:
    engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
    print("Success")
except Exception as e:
    print(f"Error: {e}")