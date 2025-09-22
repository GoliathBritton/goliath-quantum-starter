"""Database models for video processing and storage."""

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from datetime import datetime
import uuid

Base = declarative_base()


class VideoMetadata(Base):
    """Table for storing YouTube video metadata."""
    __tablename__ = "video_metadata"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Video identification
    video_id = Column(String(20), unique=True, nullable=False, index=True)
    url = Column(String(500), nullable=False)
    
    # Basic metadata
    title = Column(Text)
    description = Column(Text)
    channel_name = Column(String(200))
    duration = Column(String(20))  # Format: "HH:MM:SS"
    view_count = Column(Integer)
    upload_date = Column(String(50))
    thumbnail_url = Column(String(500))
    
    # Processing metadata
    processing_status = Column(String(20), default='pending')  # pending, success, failed
    processing_error = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analysis = relationship("VideoAnalysis", back_populates="video", uselist=False)
    tags = relationship("VideoTag", back_populates="video")
    
    def __repr__(self):
        return f"<VideoMetadata(video_id='{self.video_id}', title='{self.title[:50]}...')>"


class VideoAnalysis(Base):
    """Table for storing video content analysis results."""
    __tablename__ = "video_analysis"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to video
    video_id = Column(UUID(as_uuid=True), ForeignKey('video_metadata.id'), nullable=False)
    
    # Analysis results
    quantum_relevance_score = Column(Float, default=0.0)
    educational_content = Column(Boolean, default=False)
    technical_level = Column(String(20))  # beginner, intermediate, advanced
    content_type = Column(String(50))  # tutorial, lecture, demo, theory, general
    
    # Keywords and concepts (stored as JSON arrays)
    keywords = Column(JSON, default=list)
    topics = Column(JSON, default=list)
    key_concepts = Column(JSON, default=list)
    
    # Analysis metadata
    analysis_version = Column(String(10), default='1.0')
    confidence_score = Column(Float, default=0.0)
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("VideoMetadata", back_populates="analysis")
    
    def __repr__(self):
        return f"<VideoAnalysis(video_id='{self.video_id}', relevance={self.quantum_relevance_score})>"


class VideoTag(Base):
    """Table for video tagging and categorization."""
    __tablename__ = "video_tags"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to video
    video_id = Column(UUID(as_uuid=True), ForeignKey('video_metadata.id'), nullable=False)
    
    # Tag information
    tag_name = Column(String(100), nullable=False)
    tag_category = Column(String(50))  # quantum_concept, algorithm, hardware, application
    confidence = Column(Float, default=1.0)
    
    # Tag metadata
    auto_generated = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    video = relationship("VideoMetadata", back_populates="tags")
    
    def __repr__(self):
        return f"<VideoTag(tag_name='{self.tag_name}', category='{self.tag_category}')>"


class VideoCollection(Base):
    """Table for organizing videos into collections."""
    __tablename__ = "video_collections"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Collection information
    name = Column(String(200), nullable=False)
    description = Column(Text)
    collection_type = Column(String(50))  # playlist, course, topic, custom
    
    # Collection metadata
    is_public = Column(Boolean, default=False)
    created_by = Column(String(100))  # User ID or system
    
    # Statistics
    video_count = Column(Integer, default=0)
    total_duration = Column(String(20))  # Calculated total duration
    avg_relevance_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    videos = relationship("VideoCollectionItem", back_populates="collection")
    
    def __repr__(self):
        return f"<VideoCollection(name='{self.name}', video_count={self.video_count})>"


class VideoCollectionItem(Base):
    """Association table for videos in collections."""
    __tablename__ = "video_collection_items"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    collection_id = Column(UUID(as_uuid=True), ForeignKey('video_collections.id'), nullable=False)
    video_id = Column(UUID(as_uuid=True), ForeignKey('video_metadata.id'), nullable=False)
    
    # Item metadata
    order_index = Column(Integer, default=0)
    notes = Column(Text)
    
    # Timestamps
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    collection = relationship("VideoCollection", back_populates="videos")
    video = relationship("VideoMetadata")
    
    def __repr__(self):
        return f"<VideoCollectionItem(collection_id='{self.collection_id}', video_id='{self.video_id}')>"


class ProcessingJob(Base):
    """Table for tracking video processing jobs."""
    __tablename__ = "processing_jobs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Job information
    job_type = Column(String(50), nullable=False)  # single_video, batch_process, collection_update
    status = Column(String(20), default='pending')  # pending, running, completed, failed
    
    # Job parameters (stored as JSON)
    parameters = Column(JSON, default=dict)
    
    # Progress tracking
    total_items = Column(Integer, default=0)
    processed_items = Column(Integer, default=0)
    failed_items = Column(Integer, default=0)
    
    # Results and errors
    results = Column(JSON, default=dict)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<ProcessingJob(job_type='{self.job_type}', status='{self.status}')>"


class VideoStatistics(Base):
    """Table for storing aggregated video statistics."""
    __tablename__ = "video_statistics"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Statistics period
    period_type = Column(String(20), nullable=False)  # daily, weekly, monthly
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Video counts
    total_videos = Column(Integer, default=0)
    new_videos = Column(Integer, default=0)
    quantum_relevant_videos = Column(Integer, default=0)
    educational_videos = Column(Integer, default=0)
    
    # Quality metrics
    avg_relevance_score = Column(Float, default=0.0)
    processing_success_rate = Column(Float, default=0.0)
    
    # Popular content
    top_keywords = Column(JSON, default=list)
    top_concepts = Column(JSON, default=list)
    technical_level_distribution = Column(JSON, default=dict)
    content_type_distribution = Column(JSON, default=dict)
    
    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<VideoStatistics(period='{self.period_type}', total_videos={self.total_videos})>"