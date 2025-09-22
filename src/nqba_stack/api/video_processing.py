"""Video processing API endpoints for YouTube video analysis and integration."""

import logging
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field, HttpUrl
import time

# Import video processing modules
try:
    from ...video_processing import VideoProcessor
except ImportError:
    # Fallback import path
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.video_processing import VideoProcessor

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["Video Processing"])

# Initialize video processor
video_processor = VideoProcessor()


# Pydantic models
class VideoURL(BaseModel):
    """Single video URL input model."""
    url: str = Field(..., description="YouTube video URL")


class VideoURLList(BaseModel):
    """Multiple video URLs input model."""
    urls: List[str] = Field(..., description="List of YouTube video URLs")
    min_relevance: Optional[float] = Field(0.3, description="Minimum quantum relevance score (0-1)")


class VideoAnalysisResponse(BaseModel):
    """Video analysis response model."""
    url: str
    metadata: Dict
    analysis: Dict
    processing_status: str


class VideoSummaryResponse(BaseModel):
    """Video summary report response model."""
    total_videos_processed: int
    successful_processing: int
    quantum_relevant_videos: int
    processing_success_rate: float
    quantum_relevance_rate: float
    technical_level_distribution: Dict
    content_type_distribution: Dict
    top_keywords: List[tuple]
    top_concepts: List[tuple]
    detailed_results: List[Dict]


@router.post("/video/analyze", response_model=VideoAnalysisResponse)
async def analyze_single_video(video_data: VideoURL):
    """Analyze a single YouTube video for quantum computing content."""
    try:
        logger.info(f"Analyzing video: {video_data.url}")
        
        result = video_processor.process_video_url(video_data.url)
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        logger.info(f"Successfully analyzed video: {video_data.url}")
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing video {video_data.url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze video: {str(e)}")


@router.post("/video/analyze-batch", response_model=List[VideoAnalysisResponse])
async def analyze_multiple_videos(video_data: VideoURLList):
    """Analyze multiple YouTube videos for quantum computing content."""
    try:
        logger.info(f"Analyzing {len(video_data.urls)} videos")
        
        results = video_processor.process_multiple_urls(video_data.urls)
        
        logger.info(f"Successfully analyzed {len(results)} videos")
        return results
        
    except Exception as e:
        logger.error(f"Error analyzing videos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze videos: {str(e)}")


@router.post("/video/quantum-relevant", response_model=List[VideoAnalysisResponse])
async def get_quantum_relevant_videos(video_data: VideoURLList):
    """Filter and return videos with high quantum computing relevance."""
    try:
        logger.info(f"Filtering {len(video_data.urls)} videos for quantum relevance (min: {video_data.min_relevance})")
        
        relevant_videos = video_processor.get_quantum_relevant_videos(
            video_data.urls, 
            min_relevance=video_data.min_relevance
        )
        
        logger.info(f"Found {len(relevant_videos)} quantum-relevant videos")
        return relevant_videos
        
    except Exception as e:
        logger.error(f"Error filtering quantum-relevant videos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to filter videos: {str(e)}")


@router.post("/video/educational", response_model=List[VideoAnalysisResponse])
async def get_educational_content(video_data: VideoURLList):
    """Filter and return educational quantum computing videos."""
    try:
        logger.info(f"Filtering {len(video_data.urls)} videos for educational content")
        
        educational_videos = video_processor.get_educational_content(video_data.urls)
        
        logger.info(f"Found {len(educational_videos)} educational videos")
        return educational_videos
        
    except Exception as e:
        logger.error(f"Error filtering educational videos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to filter educational videos: {str(e)}")


@router.post("/video/summary-report", response_model=VideoSummaryResponse)
async def generate_summary_report(video_data: VideoURLList):
    """Generate a comprehensive summary report for all provided videos."""
    try:
        logger.info(f"Generating summary report for {len(video_data.urls)} videos")
        
        summary = video_processor.generate_summary_report(video_data.urls)
        
        logger.info("Successfully generated summary report")
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary report: {str(e)}")


@router.post("/video/export")
async def export_video_data(video_data: VideoURLList, background_tasks: BackgroundTasks):
    """Export video analysis data to JSON file."""
    try:
        logger.info(f"Exporting data for {len(video_data.urls)} videos")
        
        # Generate summary report
        summary = video_processor.generate_summary_report(video_data.urls)
        
        # Create filename with timestamp
        timestamp = int(time.time())
        filename = f"video_analysis_export_{timestamp}.json"
        
        # Export in background
        def export_task():
            success = video_processor.export_to_json(summary, filename)
            if success:
                logger.info(f"Successfully exported data to {filename}")
            else:
                logger.error(f"Failed to export data to {filename}")
        
        background_tasks.add_task(export_task)
        
        return {
            "status": "success",
            "message": "Export task started",
            "filename": filename,
            "timestamp": timestamp
        }
        
    except Exception as e:
        logger.error(f"Error starting export task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start export: {str(e)}")


@router.get("/video/health")
async def video_processing_health():
    """Health check endpoint for video processing service."""
    try:
        # Test basic functionality
        test_result = video_processor.extractor.extract_video_id(
            "https://www.youtube.com/watch?v=test123"
        )
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "video_processing",
            "components": {
                "video_extractor": "operational",
                "content_analyzer": "operational",
                "video_processor": "operational"
            },
            "test_extraction": test_result == "test123"
        }
        
    except Exception as e:
        logger.error(f"Video processing health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "service": "video_processing",
            "error": str(e)
        }


@router.get("/video/stats")
async def get_video_processing_stats():
    """Get video processing service statistics and capabilities."""
    try:
        return {
            "status": "success",
            "timestamp": time.time(),
            "capabilities": {
                "supported_platforms": ["YouTube"],
                "analysis_features": [
                    "Quantum relevance scoring",
                    "Educational content detection",
                    "Technical level assessment",
                    "Content type classification",
                    "Keyword extraction",
                    "Concept identification"
                ],
                "output_formats": ["JSON", "Summary Report"],
                "batch_processing": True,
                "background_export": True
            },
            "quantum_keywords": {
                "basic": ["quantum", "qubit", "superposition", "entanglement", "measurement"],
                "algorithms": ["grover", "shor", "deutsch", "bernstein", "vazirani", "simon"],
                "gates": ["hadamard", "pauli", "cnot", "toffoli", "rotation", "phase"],
                "concepts": ["interference", "decoherence", "fidelity", "bloch sphere", "bell state"],
                "applications": ["cryptography", "optimization", "simulation", "machine learning"],
                "hardware": ["ibm", "google", "rigetti", "ionq", "superconducting", "trapped ion"]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting video processing stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")