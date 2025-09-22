"""YouTube video data extraction module."""

import re
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs


@dataclass
class VideoMetadata:
    """Data class for storing video metadata."""
    video_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None
    channel_name: Optional[str] = None
    tags: List[str] = None
    thumbnail_url: Optional[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class VideoExtractor:
    """Extracts metadata and content from YouTube videos."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_metadata(self, video_id: str) -> VideoMetadata:
        """Get basic video metadata."""
        # Create metadata object with video ID
        metadata = VideoMetadata(video_id=video_id)
        
        try:
            # Try to get basic info from YouTube page
            url = f"https://www.youtube.com/watch?v={video_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text
                
                # Extract title
                title_match = re.search(r'<title>([^<]+)</title>', content)
                if title_match:
                    metadata.title = title_match.group(1).replace(' - YouTube', '')
                
                # Extract description (basic)
                desc_match = re.search(r'"description":{"simpleText":"([^"]+)"', content)
                if desc_match:
                    metadata.description = desc_match.group(1)
                
                # Extract channel name
                channel_match = re.search(r'"ownerChannelName":"([^"]+)"', content)
                if channel_match:
                    metadata.channel_name = channel_match.group(1)
                
                # Set thumbnail URL
                metadata.thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                
        except Exception as e:
            print(f"Error extracting metadata for {video_id}: {e}")
        
        return metadata
    
    def process_video_urls(self, urls: List[str]) -> List[VideoMetadata]:
        """Process multiple video URLs and extract metadata."""
        results = []
        
        for url in urls:
            video_id = self.extract_video_id(url)
            if video_id:
                metadata = self.get_video_metadata(video_id)
                results.append(metadata)
            else:
                print(f"Could not extract video ID from: {url}")
        
        return results
    
    def get_video_info_dict(self, video_id: str) -> Dict:
        """Get video information as dictionary."""
        metadata = self.get_video_metadata(video_id)
        return {
            'video_id': metadata.video_id,
            'title': metadata.title,
            'description': metadata.description,
            'duration': metadata.duration,
            'view_count': metadata.view_count,
            'upload_date': metadata.upload_date,
            'channel_name': metadata.channel_name,
            'tags': metadata.tags,
            'thumbnail_url': metadata.thumbnail_url
        }