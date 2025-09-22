"""Content analysis module for processing video data."""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from .video_extractor import VideoMetadata

from .categorization import tag_manager, categorizer


@dataclass
class ContentAnalysis:
    """Results of content analysis."""
    keywords: List[str]
    topics: List[str]
    quantum_relevance_score: float
    educational_content: bool
    technical_level: str  # 'beginner', 'intermediate', 'advanced'
    content_type: str  # 'tutorial', 'lecture', 'demo', 'theory'
    key_concepts: List[str]
    confidence_score: float = 0.0
    tags: List[str] = None
    primary_category: str = None
    secondary_categories: List[str] = None
    
    def __post_init__(self):
        """Initialize optional fields."""
        if self.tags is None:
            self.tags = []
        if self.secondary_categories is None:
            self.secondary_categories = []
    

class ContentAnalyzer:
    """Analyzes video content for quantum computing relevance and educational value."""
    
    def __init__(self):
        # Quantum computing keywords and concepts
        self.quantum_keywords = {
            'basic': ['quantum', 'qubit', 'superposition', 'entanglement', 'measurement'],
            'algorithms': ['grover', 'shor', 'deutsch', 'bernstein', 'vazirani', 'simon'],
            'gates': ['hadamard', 'pauli', 'cnot', 'toffoli', 'rotation', 'phase'],
            'concepts': ['interference', 'decoherence', 'fidelity', 'bloch sphere', 'bell state'],
            'applications': ['cryptography', 'optimization', 'simulation', 'machine learning'],
            'hardware': ['ibm', 'google', 'rigetti', 'ionq', 'superconducting', 'trapped ion']
        }
        
        self.educational_indicators = [
            'tutorial', 'learn', 'introduction', 'beginner', 'guide', 'course',
            'lesson', 'explain', 'understand', 'basics', 'fundamentals'
        ]
        
        self.technical_indicators = {
            'beginner': ['introduction', 'basics', 'beginner', 'start', 'first'],
            'intermediate': ['implementation', 'algorithm', 'programming', 'code'],
            'advanced': ['research', 'paper', 'theory', 'proof', 'mathematical']
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        if not text:
            return []
        
        text_lower = text.lower()
        keywords = []
        
        # Check for quantum keywords
        for category, words in self.quantum_keywords.items():
            for word in words:
                if word in text_lower:
                    keywords.append(word)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(keywords))
    
    def calculate_quantum_relevance(self, metadata: VideoMetadata) -> float:
        """Calculate quantum computing relevance score (0-1)."""
        score = 0.0
        total_text = f"{metadata.title or ''} {metadata.description or ''}".lower()
        
        if not total_text.strip():
            return 0.0
        
        # Weight different categories
        weights = {
            'basic': 0.3,
            'algorithms': 0.25,
            'gates': 0.2,
            'concepts': 0.15,
            'applications': 0.1,
            'hardware': 0.1
        }
        
        for category, words in self.quantum_keywords.items():
            category_score = 0
            for word in words:
                if word in total_text:
                    category_score += 1
            
            # Normalize by category size and apply weight
            if words:
                normalized_score = min(category_score / len(words), 1.0)
                score += normalized_score * weights.get(category, 0.1)
        
        return min(score, 1.0)
    
    def determine_technical_level(self, metadata: VideoMetadata) -> str:
        """Determine the technical level of the content."""
        total_text = f"{metadata.title or ''} {metadata.description or ''}".lower()
        
        level_scores = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
        
        for level, indicators in self.technical_indicators.items():
            for indicator in indicators:
                if indicator in total_text:
                    level_scores[level] += 1
        
        # Return level with highest score, default to intermediate
        if max(level_scores.values()) == 0:
            return 'intermediate'
        
        return max(level_scores, key=level_scores.get)
    
    def identify_content_type(self, metadata: VideoMetadata) -> str:
        """Identify the type of educational content."""
        total_text = f"{metadata.title or ''} {metadata.description or ''}".lower()
        
        type_indicators = {
            'tutorial': ['tutorial', 'how to', 'step by step', 'guide'],
            'lecture': ['lecture', 'presentation', 'talk', 'seminar'],
            'demo': ['demo', 'demonstration', 'example', 'showcase'],
            'theory': ['theory', 'mathematical', 'proof', 'derivation']
        }
        
        for content_type, indicators in type_indicators.items():
            for indicator in indicators:
                if indicator in total_text:
                    return content_type
        
        return 'general'
    
    def extract_key_concepts(self, metadata: VideoMetadata) -> List[str]:
        """Extract key quantum computing concepts from the content."""
        concepts = []
        total_text = f"{metadata.title or ''} {metadata.description or ''}".lower()
        
        # Combine all quantum keywords as potential concepts
        all_concepts = []
        for category_words in self.quantum_keywords.values():
            all_concepts.extend(category_words)
        
        for concept in all_concepts:
            if concept in total_text:
                concepts.append(concept)
        
        return list(dict.fromkeys(concepts))  # Remove duplicates
    
    def analyze_content(self, metadata: VideoMetadata) -> ContentAnalysis:
        """Perform comprehensive content analysis."""
        title = metadata.title or ""
        description = metadata.description or ""
        channel_name = getattr(metadata, 'channel_name', '') or ""
        
        # Use the new categorization system
        categorization_result = tag_manager.generate_comprehensive_tags(
            title, description, channel_name
        )
        
        # Calculate quantum relevance score (enhanced)
        quantum_score = self.calculate_quantum_relevance(metadata)
        
        # Use categorization results to enhance analysis
        is_educational = (
            categorization_result['content_type'] in ['tutorial', 'lecture', 'demonstration'] or
            any(indicator in f"{title} {description}".lower() for indicator in self.educational_indicators)
        )
        
        # Map technical level from categorization
        tech_level_mapping = {
            'beginner': 'beginner',
            'intermediate': 'intermediate', 
            'advanced': 'advanced',
            'expert': 'advanced',
            'unknown': self.determine_technical_level(metadata)
        }
        tech_level = tech_level_mapping.get(
            categorization_result['technical_level'],
            'intermediate'
        )
        
        # Extract topics (simplified - could be enhanced with NLP)
        topics = []
        if quantum_score > 0.3:
            topics.append('quantum computing')
        if any(word in f"{title} {description}".lower() for word in ['algorithm', 'programming']):
            topics.append('algorithms')
        if any(word in f"{title} {description}".lower() for word in ['hardware', 'device']):
            topics.append('hardware')
        
        # Combine with categorization concepts
        topics.extend(categorization_result['concepts'][:5])
        topics = list(dict.fromkeys(topics))  # Remove duplicates
        
        return ContentAnalysis(
            keywords=categorization_result['keywords'][:15],  # Limit keywords
            topics=topics[:10],    # Limit topics
            quantum_relevance_score=max(quantum_score, categorization_result['confidence_score']),
            educational_content=is_educational,
            technical_level=tech_level,
            content_type=categorization_result['content_type'],
            key_concepts=categorization_result['concepts'],
            confidence_score=categorization_result['confidence_score'],
            tags=categorization_result['tags'][:20],  # Add tags to analysis
            primary_category=categorization_result['primary_category'],
            secondary_categories=categorization_result['secondary_categories']
        )
    
    def analyze_multiple_videos(self, video_metadata_list: List[VideoMetadata]) -> List[ContentAnalysis]:
        """Analyze multiple videos and return analysis results."""
        return [self.analyze_content(metadata) for metadata in video_metadata_list]