from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, func
from .base import Base


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    contact = Column(String, nullable=True)
    email = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    score = Column(Float, default=0.0)
    meta = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())


class SigmaMetric(Base):
    __tablename__ = "sigma_metrics"
    id = Column(Integer, primary_key=True)
    metric = Column(String, index=True)  # qei, momentum, revenue_uplift
    value = Column(Float, default=0.0)
    window = Column(String, default="7d")
    details = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())


class QuantumPerfLog(Base):
    __tablename__ = "quantum_perf_logs"
    id = Column(Integer, primary_key=True)
    backend = Column(String, default="dynex")
    accel_nvidia = Column(Boolean, default=True)
    multiplier = Column(Float, default=410.0)
    payload = Column(JSON, default={})
    created_at = Column(DateTime, server_default=func.now())
