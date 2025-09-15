from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, Boolean, Numeric, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class OracleQuery(Base):
    """Oracle Query model for tracking quantum oracle requests and responses."""
    
    __tablename__ = "oracle_queries"
    
    # Relationships
    partner_id: Mapped[str] = mapped_column(ForeignKey("partners.id"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("leads.id"), nullable=True, index=True)
    
    # Query Information
    query_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # lead_scoring, market_prediction, risk_assessment
    query_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    query_parameters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Input Data
    input_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    input_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)  # For caching
    
    # Quantum Processing
    dynex_job_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    qubo_matrix: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    quantum_algorithm: Mapped[str] = mapped_column(String(100), default="simulated_annealing", nullable=False)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Oracle Response
    prophecy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Numeric(5, 2), nullable=True)  # 0.00 to 100.00
    recommended_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    explainability: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Structured Results
    score: Mapped[Optional[float]] = mapped_column(Numeric(8, 4), nullable=True)
    probability: Mapped[Optional[float]] = mapped_column(Numeric(5, 4), nullable=True)  # 0.0000 to 1.0000
    risk_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # low, medium, high, critical
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Query Metadata
    model_version: Mapped[str] = mapped_column(String(50), default="1.0", nullable=False)
    api_version: Mapped[str] = mapped_column(String(50), default="v1", nullable=False)
    
    # Status & Execution
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending, processing, completed, failed, cached
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Performance Metrics
    queue_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    execution_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Cost & Credits
    quantum_credits_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_usd: Mapped[Optional[float]] = mapped_column(Numeric(10, 4), nullable=True)
    
    # Caching & Optimization
    cached_result: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cache_hit: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cache_expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Feedback & Quality
    feedback_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 stars
    feedback_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    accuracy_verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    
    # Compliance & Audit
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    # Business Context
    business_impact: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # low, medium, high, critical
    urgency: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # low, normal, high, urgent
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    # partner = relationship("Partner", back_populates="oracle_queries")
    # user = relationship("User", back_populates="oracle_queries")
    # lead = relationship("Lead", back_populates="oracle_queries")
    
    def __repr__(self) -> str:
        return f"<OracleQuery(id={self.id}, type={self.query_type}, status={self.status})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if query is completed successfully."""
        return self.status == "completed"
    
    @property
    def is_failed(self) -> bool:
        """Check if query failed."""
        return self.status == "failed"
    
    @property
    def is_processing(self) -> bool:
        """Check if query is currently processing."""
        return self.status in ["pending", "processing"]
    
    @property
    def response_time_seconds(self) -> Optional[float]:
        """Get total response time in seconds."""
        if self.total_time_ms is None:
            return None
        return self.total_time_ms / 1000.0
    
    @property
    def is_high_confidence(self) -> bool:
        """Check if result has high confidence."""
        return self.confidence is not None and self.confidence >= 80.0
    
    @property
    def is_actionable(self) -> bool:
        """Check if result is actionable (high confidence + recommendation)."""
        return (
            self.is_high_confidence and 
            self.recommended_action is not None and 
            len(self.recommended_action.strip()) > 0
        )
    
    def start_processing(self) -> None:
        """Mark query as processing."""
        self.status = "processing"
        self.queue_time_ms = int((datetime.utcnow() - self.created_at).total_seconds() * 1000)
    
    def complete_successfully(self, 
                            prophecy: str,
                            confidence: float,
                            recommended_action: str,
                            explainability: str,
                            processing_time_ms: int,
                            credits_used: int = 1) -> None:
        """Mark query as completed successfully."""
        self.status = "completed"
        self.prophecy = prophecy
        self.confidence = max(0.0, min(100.0, confidence))
        self.recommended_action = recommended_action
        self.explainability = explainability
        self.processing_time_ms = processing_time_ms
        self.execution_time_ms = processing_time_ms
        self.total_time_ms = (self.queue_time_ms or 0) + processing_time_ms
        self.quantum_credits_used = credits_used
    
    def fail_with_error(self, error_message: str) -> None:
        """Mark query as failed with error."""
        self.status = "failed"
        self.error_message = error_message
        self.total_time_ms = int((datetime.utcnow() - self.created_at).total_seconds() * 1000)
    
    def mark_as_cached(self, cache_expires_at: Optional[datetime] = None) -> None:
        """Mark result as cached."""
        self.cached_result = True
        self.cache_hit = True
        self.cache_expires_at = cache_expires_at
        self.quantum_credits_used = 0  # No credits used for cached results
    
    def add_feedback(self, rating: int, comment: Optional[str] = None) -> None:
        """Add user feedback for the query result."""
        self.feedback_rating = max(1, min(5, rating))
        self.feedback_comment = comment
    
    def verify_accuracy(self, is_accurate: bool) -> None:
        """Verify the accuracy of the prediction."""
        self.accuracy_verified = is_accurate
    
    def increment_retry(self) -> None:
        """Increment retry count."""
        self.retry_count += 1
    
    def set_business_context(self, impact: str, urgency: str) -> None:
        """Set business context for the query."""
        valid_impacts = ["low", "medium", "high", "critical"]
        valid_urgencies = ["low", "normal", "high", "urgent"]
        
        if impact in valid_impacts:
            self.business_impact = impact
        
        if urgency in valid_urgencies:
            self.urgency = urgency
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the query."""
        if not self.tags:
            self.tags = []
        
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the query."""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)