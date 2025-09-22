"""Database setup and management for video processing."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os
from typing import Generator

from .models import (
    Base,
    VideoMetadata,
    VideoAnalysis,
    VideoTag,
    VideoCollection,
    VideoCollectionItem,
    ProcessingJob,
    VideoStatistics
)

# Database configuration
DATABASE_URL = os.getenv(
    "VIDEO_DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/quantum_videos"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all video processing tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Video processing tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


def drop_tables():
    """Drop all video processing tables (use with caution!)."""
    try:
        Base.metadata.drop_all(bind=engine)
        print("Video processing tables dropped successfully.")
    except Exception as e:
        print(f"Error dropping tables: {e}")
        raise


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session with automatic cleanup."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class VideoDatabase:
    """Database manager for video processing operations."""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()
    
    def create_video_metadata(self, session: Session, video_data: dict) -> VideoMetadata:
        """Create a new video metadata record."""
        video = VideoMetadata(**video_data)
        session.add(video)
        session.flush()  # Get the ID without committing
        return video
    
    def get_video_by_id(self, session: Session, video_id: str) -> VideoMetadata:
        """Get video metadata by video ID."""
        return session.query(VideoMetadata).filter(
            VideoMetadata.video_id == video_id
        ).first()
    
    def create_video_analysis(self, session: Session, analysis_data: dict) -> VideoAnalysis:
        """Create a new video analysis record."""
        analysis = VideoAnalysis(**analysis_data)
        session.add(analysis)
        session.flush()
        return analysis
    
    def add_video_tags(self, session: Session, video_id: str, tags: list) -> list:
        """Add tags to a video."""
        video = session.query(VideoMetadata).filter(
            VideoMetadata.video_id == video_id
        ).first()
        
        if not video:
            raise ValueError(f"Video with ID {video_id} not found")
        
        tag_objects = []
        for tag_data in tags:
            tag = VideoTag(
                video_id=video.id,
                **tag_data
            )
            session.add(tag)
            tag_objects.append(tag)
        
        session.flush()
        return tag_objects
    
    def get_quantum_relevant_videos(self, session: Session, min_score: float = 0.5) -> list:
        """Get videos with quantum relevance score above threshold."""
        return session.query(VideoMetadata).join(VideoAnalysis).filter(
            VideoAnalysis.quantum_relevance_score >= min_score
        ).all()
    
    def get_educational_videos(self, session: Session) -> list:
        """Get videos marked as educational content."""
        return session.query(VideoMetadata).join(VideoAnalysis).filter(
            VideoAnalysis.educational_content == True
        ).all()
    
    def create_collection(self, session: Session, collection_data: dict) -> VideoCollection:
        """Create a new video collection."""
        collection = VideoCollection(**collection_data)
        session.add(collection)
        session.flush()
        return collection
    
    def add_video_to_collection(self, session: Session, collection_id: str, video_id: str, order_index: int = 0) -> VideoCollectionItem:
        """Add a video to a collection."""
        item = VideoCollectionItem(
            collection_id=collection_id,
            video_id=video_id,
            order_index=order_index
        )
        session.add(item)
        session.flush()
        return item
    
    def create_processing_job(self, session: Session, job_data: dict) -> ProcessingJob:
        """Create a new processing job record."""
        job = ProcessingJob(**job_data)
        session.add(job)
        session.flush()
        return job
    
    def update_processing_job(self, session: Session, job_id: str, updates: dict) -> ProcessingJob:
        """Update a processing job."""
        job = session.query(ProcessingJob).filter(
            ProcessingJob.id == job_id
        ).first()
        
        if not job:
            raise ValueError(f"Processing job with ID {job_id} not found")
        
        for key, value in updates.items():
            setattr(job, key, value)
        
        session.flush()
        return job
    
    def get_video_statistics(self, session: Session, period_type: str = None) -> list:
        """Get video statistics, optionally filtered by period type."""
        query = session.query(VideoStatistics)
        
        if period_type:
            query = query.filter(VideoStatistics.period_type == period_type)
        
        return query.order_by(VideoStatistics.period_start.desc()).all()
    
    def search_videos(self, session: Session, **filters) -> list:
        """Search videos with various filters."""
        query = session.query(VideoMetadata)
        
        # Join with analysis if needed
        if any(key in filters for key in ['quantum_relevance_score', 'educational_content', 'technical_level']):
            query = query.join(VideoAnalysis)
        
        # Apply filters
        if 'title_contains' in filters:
            query = query.filter(VideoMetadata.title.ilike(f"%{filters['title_contains']}%"))
        
        if 'channel_name' in filters:
            query = query.filter(VideoMetadata.channel_name == filters['channel_name'])
        
        if 'quantum_relevance_score' in filters:
            query = query.filter(VideoAnalysis.quantum_relevance_score >= filters['quantum_relevance_score'])
        
        if 'educational_content' in filters:
            query = query.filter(VideoAnalysis.educational_content == filters['educational_content'])
        
        if 'technical_level' in filters:
            query = query.filter(VideoAnalysis.technical_level == filters['technical_level'])
        
        return query.all()
    
    def save_video(self, session: Session, video_id: str, url: str, metadata, analysis) -> VideoMetadata:
        """Save complete video data (metadata and analysis) to database."""
        # Create video metadata record
        video_data = {
            'video_id': video_id,
            'url': url,
            'title': metadata.title,
            'description': metadata.description,
            'channel_name': metadata.channel_name,
            'duration': metadata.duration,
            'view_count': metadata.view_count,
            'upload_date': metadata.upload_date,
            'thumbnail_url': metadata.thumbnail_url,
            'processing_status': 'success'
        }
        
        video = self.create_video_metadata(session, video_data)
        
        # Create analysis record
        analysis_data = {
            'video_id': video.id,
            'quantum_relevance_score': analysis.quantum_relevance_score,
            'educational_content': analysis.educational_content,
            'technical_level': analysis.technical_level,
            'content_type': analysis.content_type,
            'keywords': analysis.keywords,
            'topics': analysis.topics,
            'key_concepts': analysis.key_concepts,
            'confidence_score': analysis.confidence_score
        }
        
        self.create_video_analysis(session, analysis_data)
        
        # Create tags if any
        if hasattr(analysis, 'tags') and analysis.tags:
            tag_data = [{
                'tag_name': tag,
                'tag_category': 'auto_generated',
                'confidence': 1.0,
                'auto_generated': True
            } for tag in analysis.tags]
            
            self.add_video_tags(session, video.video_id, tag_data)
        
        session.flush()
        return video
    
    def save_failed_video(self, session: Session, video_id: str, url: str, error_message: str) -> VideoMetadata:
        """Save failed video processing record."""
        video_data = {
            'video_id': video_id,
            'url': url,
            'processing_status': 'failed',
            'processing_error': error_message
        }
        
        video = self.create_video_metadata(session, video_data)
        session.flush()
        return video


# Global database instance
video_db = VideoDatabase()


def init_video_database():
    """Initialize the video processing database."""
    try:
        create_tables()
        print("Video processing database initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize video processing database: {e}")
        raise


if __name__ == "__main__":
    # Create tables when run directly
    init_video_database()