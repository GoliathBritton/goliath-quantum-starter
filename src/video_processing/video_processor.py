"""Main video processing module that combines extraction and analysis."""

import json
from typing import Dict, List, Optional
from dataclasses import asdict
from datetime import datetime
import uuid
from .video_extractor import VideoExtractor, VideoMetadata
from .content_analyzer import ContentAnalyzer, ContentAnalysis
from .database import video_db, get_db_session
from .models import VideoMetadata, VideoAnalysis, VideoTag


class VideoProcessor:
    """Main class for processing YouTube videos - extraction and analysis."""
    
    def __init__(self, use_database: bool = True):
        self.extractor = VideoExtractor()
        self.analyzer = ContentAnalyzer()
        self.use_database = use_database
    
    def process_video_url(self, url: str) -> Dict:
        """Process a single video URL and return complete analysis."""
        # Extract video ID
        video_id = self.extractor.extract_video_id(url)
        if not video_id:
            return {'error': f'Could not extract video ID from URL: {url}'}
        
        # Check if video already exists in database
        if self.use_database:
            with get_db_session() as session:
                existing_video = video_db.get_video_by_id(session, video_id)
                if existing_video and existing_video.processing_status == 'success':
                    # Return existing data
                    analysis = session.query(VideoAnalysis).filter(
                        VideoAnalysis.video_id == existing_video.id
                    ).first()
                    
                    return {
                        'url': url,
                        'metadata': asdict(existing_video),
                        'analysis': asdict(analysis) if analysis else {},
                        'processing_status': 'success',
                        'from_database': True
                    }
        
        # Get metadata
        metadata = self.extractor.get_video_metadata(video_id)
        
        # Analyze content
        analysis = self.analyzer.analyze_content(metadata)
        
        # Save to database if enabled
        if self.use_database:
            self._save_video_to_database(video_id, url, metadata, analysis)
        
        # Combine results
        result = {
            'url': url,
            'metadata': asdict(metadata),
            'analysis': asdict(analysis),
            'processing_status': 'success',
            'from_database': False
        }
        
        return result
    
    def process_multiple_urls(self, urls: List[str]) -> List[Dict]:
        """Process multiple video URLs."""
        results = []
        
        for url in urls:
            try:
                result = self.process_video_url(url)
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'processing_status': 'failed'
                })
        
        return results
    
    def get_quantum_relevant_videos(self, urls: List[str], min_relevance: float = 0.3) -> List[Dict]:
        """Filter videos by quantum computing relevance score."""
        all_results = self.process_multiple_urls(urls)
        
        relevant_videos = []
        for result in all_results:
            if 'analysis' in result:
                relevance_score = result['analysis'].get('quantum_relevance_score', 0)
                if relevance_score >= min_relevance:
                    relevant_videos.append(result)
        
        # Sort by relevance score (highest first)
        relevant_videos.sort(
            key=lambda x: x['analysis'].get('quantum_relevance_score', 0),
            reverse=True
        )
        
        return relevant_videos
    
    def generate_summary_report(self, urls: List[str]) -> Dict:
        """Generate a comprehensive summary report for all videos."""
        results = self.process_multiple_urls(urls)
        
        # Initialize counters
        total_videos = len(results)
        successful_processing = sum(1 for r in results if r.get('processing_status') == 'success')
        quantum_relevant = sum(1 for r in results 
                             if 'analysis' in r and r['analysis'].get('quantum_relevance_score', 0) > 0.3)
        
        # Collect statistics
        technical_levels = {}
        content_types = {}
        all_keywords = []
        all_concepts = []
        
        for result in results:
            if 'analysis' in result:
                analysis = result['analysis']
                
                # Technical level distribution
                level = analysis.get('technical_level', 'unknown')
                technical_levels[level] = technical_levels.get(level, 0) + 1
                
                # Content type distribution
                content_type = analysis.get('content_type', 'unknown')
                content_types[content_type] = content_types.get(content_type, 0) + 1
                
                # Collect keywords and concepts
                all_keywords.extend(analysis.get('keywords', []))
                all_concepts.extend(analysis.get('key_concepts', []))
        
        # Count frequency of keywords and concepts
        keyword_freq = {}
        for keyword in all_keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        concept_freq = {}
        for concept in all_concepts:
            concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
        # Create summary
        summary = {
            'total_videos_processed': total_videos,
            'successful_processing': successful_processing,
            'quantum_relevant_videos': quantum_relevant,
            'processing_success_rate': successful_processing / total_videos if total_videos > 0 else 0,
            'quantum_relevance_rate': quantum_relevant / successful_processing if successful_processing > 0 else 0,
            'technical_level_distribution': technical_levels,
            'content_type_distribution': content_types,
            'top_keywords': sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10],
            'top_concepts': sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)[:10],
            'detailed_results': results
        }
        
        return summary
    
    def _save_video_to_database(self, video_id: str, url: str, metadata: VideoMetadata, analysis: ContentAnalysis) -> None:
        """Save video data to database."""
        try:
            with get_db_session() as session:
                video_db.save_video(session, video_id, url, metadata, analysis)
        except Exception as e:
            print(f"Error saving video to database: {e}")
    
    def _save_failed_video(self, video_id: str, url: str, error_message: str) -> None:
        """Save failed video processing to database."""
        try:
            with get_db_session() as session:
                video_db.save_failed_video(session, video_id, url, error_message)
        except Exception as e:
            print(f"Error saving failed video to database: {e}")
    
    def export_to_json(self, data: Dict, filename: str) -> bool:
        """Export processed data to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def get_educational_content(self, urls: List[str]) -> List[Dict]:
        """Filter and return educational quantum computing content."""
        if self.use_database:
            try:
                with get_db_session() as session:
                    videos = video_db.get_educational_videos(session)
                    educational_videos = []
                    
                    for video in videos:
                        analysis = session.query(VideoAnalysis).filter(
                            VideoAnalysis.video_id == video.id
                        ).first()
                        
                        if analysis and analysis.quantum_relevance_score > 0.2:
                            educational_videos.append({
                                'url': video.url,
                                'metadata': asdict(video),
                                'analysis': asdict(analysis),
                                'processing_status': 'success'
                            })
                    
                    return educational_videos
            except Exception as e:
                print(f"Database error in get_educational_content: {e}")
                # Fall back to processing URLs
        
        # Process URLs directly (fallback or when database is disabled)
        all_results = self.process_multiple_urls(urls)
        
        educational_videos = []
        for result in all_results:
            if 'analysis' in result:
                analysis = result['analysis']
                if (analysis.get('educational_content', False) and 
                    analysis.get('quantum_relevance_score', 0) > 0.2):
                    educational_videos.append(result)
        
        return educational_videos