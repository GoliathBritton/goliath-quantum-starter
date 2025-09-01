import os
from pydantic import BaseModel


class QuantumConfig(BaseModel):
    preferred_backend: str = os.getenv("QUANTUM_BACKEND", "dynex")
    dynex_enabled: bool = True
    nvidia_accel: bool = True
    performance_multiplier: float = 410.0  # Dynex baseline


class Settings(BaseModel):
    project_name: str = "FLYFOX AI — Sigma Select"
    api_prefix: str = "/api"
    sql_url: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/sigma"
    )
    quantum: QuantumConfig = QuantumConfig()


settings = Settings()
