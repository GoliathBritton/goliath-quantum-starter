"""Video content categorization and tagging system."""

import re
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class QuantumCategory(Enum):
    """Quantum computing categories."""
    FUNDAMENTALS = "fundamentals"
    ALGORITHMS = "algorithms"
    HARDWARE = "hardware"
    APPLICATIONS = "applications"
    PROGRAMMING = "programming"
    THEORY = "theory"
    CRYPTOGRAPHY = "cryptography"
    MACHINE_LEARNING = "machine_learning"
    NETWORKING = "networking"
    ERROR_CORRECTION = "error_correction"
    GENERAL = "general"


class TechnicalLevel(Enum):
    """Technical difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
    UNKNOWN = "unknown"


class ContentType(Enum):
    """Content type classifications."""
    TUTORIAL = "tutorial"
    LECTURE = "lecture"
    DEMONSTRATION = "demonstration"
    INTERVIEW = "interview"
    CONFERENCE_TALK = "conference_talk"
    DOCUMENTARY = "documentary"
    NEWS = "news"
    REVIEW = "review"
    GENERAL = "general"


@dataclass
class CategoryResult:
    """Result of categorization analysis."""
    primary_category: QuantumCategory
    secondary_categories: List[QuantumCategory]
    technical_level: TechnicalLevel
    content_type: ContentType
    confidence_score: float
    tags: List[str]
    keywords: List[str]
    concepts: List[str]


class QuantumContentCategorizer:
    """Categorizes quantum computing video content."""
    
    def __init__(self):
        self.quantum_keywords = self._load_quantum_keywords()
        self.technical_indicators = self._load_technical_indicators()
        self.content_type_patterns = self._load_content_type_patterns()
    
    def categorize_content(self, title: str, description: str, channel_name: str = "") -> CategoryResult:
        """Categorize video content based on title, description, and channel."""
        text = f"{title} {description} {channel_name}".lower()
        
        # Determine primary and secondary categories
        categories = self._identify_categories(text)
        primary_category = categories[0] if categories else QuantumCategory.GENERAL
        secondary_categories = categories[1:3] if len(categories) > 1 else []
        
        # Determine technical level
        technical_level = self._determine_technical_level(text)
        
        # Determine content type
        content_type = self._determine_content_type(title, description)
        
        # Extract keywords and concepts
        keywords = self._extract_keywords(text)
        concepts = self._extract_concepts(text)
        
        # Generate tags
        tags = self._generate_tags(primary_category, secondary_categories, technical_level, content_type)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(text, categories, keywords)
        
        return CategoryResult(
            primary_category=primary_category,
            secondary_categories=secondary_categories,
            technical_level=technical_level,
            content_type=content_type,
            confidence_score=confidence_score,
            tags=tags,
            keywords=keywords,
            concepts=concepts
        )
    
    def _load_quantum_keywords(self) -> Dict[QuantumCategory, List[str]]:
        """Load quantum computing keywords by category."""
        return {
            QuantumCategory.FUNDAMENTALS: [
                "qubit", "superposition", "entanglement", "quantum state", "wave function",
                "quantum mechanics", "quantum physics", "quantum basics", "introduction",
                "fundamentals", "principles", "quantum 101", "quantum computing basics"
            ],
            QuantumCategory.ALGORITHMS: [
                "shor's algorithm", "grover's algorithm", "quantum algorithm", "vqe", "qaoa",
                "quantum fourier transform", "quantum search", "quantum optimization",
                "variational quantum", "quantum approximate", "quantum simulation",
                "quantum phase estimation", "quantum counting"
            ],
            QuantumCategory.HARDWARE: [
                "quantum computer", "quantum processor", "quantum chip", "superconducting",
                "trapped ion", "photonic", "quantum annealing", "quantum gate",
                "quantum circuit", "ibm quantum", "google quantum", "rigetti",
                "ionq", "quantum hardware", "quantum device", "quantum system"
            ],
            QuantumCategory.APPLICATIONS: [
                "quantum application", "quantum use case", "quantum advantage",
                "quantum supremacy", "quantum finance", "quantum chemistry",
                "quantum drug discovery", "quantum logistics", "quantum sensing",
                "quantum metrology", "quantum imaging", "quantum radar"
            ],
            QuantumCategory.PROGRAMMING: [
                "qiskit", "cirq", "pennylane", "quantum programming", "quantum code",
                "quantum software", "quantum development", "quantum sdk",
                "quantum framework", "quantum library", "quantum python",
                "quantum simulator", "quantum compiler"
            ],
            QuantumCategory.THEORY: [
                "quantum theory", "quantum information", "quantum complexity",
                "quantum computational complexity", "quantum shannon theory",
                "quantum channel", "quantum entropy", "quantum fidelity",
                "quantum discord", "quantum coherence", "decoherence"
            ],
            QuantumCategory.CRYPTOGRAPHY: [
                "quantum cryptography", "quantum key distribution", "post-quantum",
                "quantum resistant", "quantum safe", "quantum security",
                "bb84", "quantum random", "quantum encryption"
            ],
            QuantumCategory.MACHINE_LEARNING: [
                "quantum machine learning", "quantum ml", "quantum neural network",
                "quantum ai", "quantum data", "quantum feature map",
                "quantum kernel", "quantum classifier", "variational quantum classifier"
            ],
            QuantumCategory.NETWORKING: [
                "quantum network", "quantum internet", "quantum communication",
                "quantum teleportation", "quantum repeater", "quantum node",
                "quantum protocol", "distributed quantum"
            ],
            QuantumCategory.ERROR_CORRECTION: [
                "quantum error correction", "quantum error", "error correction",
                "surface code", "stabilizer code", "quantum fault tolerance",
                "logical qubit", "error mitigation", "noise model"
            ]
        }
    
    def _load_technical_indicators(self) -> Dict[TechnicalLevel, List[str]]:
        """Load technical level indicators."""
        return {
            TechnicalLevel.BEGINNER: [
                "introduction", "basics", "beginner", "101", "explained", "simple",
                "easy", "start", "learn", "tutorial", "guide", "overview",
                "what is", "how to", "getting started", "for dummies"
            ],
            TechnicalLevel.INTERMEDIATE: [
                "intermediate", "implementation", "programming", "coding",
                "practical", "hands-on", "workshop", "example", "case study",
                "application", "project", "building", "developing"
            ],
            TechnicalLevel.ADVANCED: [
                "advanced", "deep dive", "research", "paper", "analysis",
                "optimization", "performance", "scalability", "architecture",
                "design", "engineering", "technical", "detailed"
            ],
            TechnicalLevel.EXPERT: [
                "expert", "cutting edge", "breakthrough", "novel", "state-of-the-art",
                "frontier", "theoretical", "mathematical", "proof", "theorem",
                "complexity theory", "formal", "rigorous"
            ]
        }
    
    def _load_content_type_patterns(self) -> Dict[ContentType, List[str]]:
        """Load content type patterns."""
        return {
            ContentType.TUTORIAL: [
                "tutorial", "how to", "step by step", "guide", "walkthrough",
                "learn", "teach", "instruction", "lesson", "course"
            ],
            ContentType.LECTURE: [
                "lecture", "class", "university", "professor", "academic",
                "course", "semester", "education", "school", "mit", "stanford"
            ],
            ContentType.DEMONSTRATION: [
                "demo", "demonstration", "show", "example", "live",
                "hands-on", "practical", "experiment", "test", "run"
            ],
            ContentType.INTERVIEW: [
                "interview", "conversation", "talk with", "discussion",
                "chat", "q&a", "questions", "answers", "podcast"
            ],
            ContentType.CONFERENCE_TALK: [
                "conference", "keynote", "presentation", "talk", "summit",
                "symposium", "workshop", "seminar", "meetup", "event"
            ],
            ContentType.DOCUMENTARY: [
                "documentary", "history", "story", "journey", "evolution",
                "timeline", "development", "behind the scenes"
            ],
            ContentType.NEWS: [
                "news", "update", "announcement", "breakthrough", "discovery",
                "latest", "recent", "new", "today", "this week"
            ],
            ContentType.REVIEW: [
                "review", "analysis", "comparison", "evaluation", "assessment",
                "critique", "opinion", "thoughts", "verdict"
            ]
        }
    
    def _identify_categories(self, text: str) -> List[QuantumCategory]:
        """Identify quantum categories based on keyword matching."""
        category_scores = {}
        
        for category, keywords in self.quantum_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Weight longer keywords more heavily
                    score += len(keyword.split())
            category_scores[category] = score
        
        # Sort by score and return top categories
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return categories with non-zero scores
        return [cat for cat, score in sorted_categories if score > 0]
    
    def _determine_technical_level(self, text: str) -> TechnicalLevel:
        """Determine technical level based on indicators."""
        level_scores = {}
        
        for level, indicators in self.technical_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text)
            level_scores[level] = score
        
        # Return level with highest score
        if max(level_scores.values()) == 0:
            return TechnicalLevel.UNKNOWN
        
        return max(level_scores.items(), key=lambda x: x[1])[0]
    
    def _determine_content_type(self, title: str, description: str) -> ContentType:
        """Determine content type based on patterns."""
        text = f"{title} {description}".lower()
        type_scores = {}
        
        for content_type, patterns in self.content_type_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text)
            type_scores[content_type] = score
        
        # Return type with highest score
        if max(type_scores.values()) == 0:
            return ContentType.GENERAL
        
        return max(type_scores.items(), key=lambda x: x[1])[0]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        keywords = set()
        
        # Extract all quantum-related keywords found in text
        for category_keywords in self.quantum_keywords.values():
            for keyword in category_keywords:
                if keyword in text:
                    keywords.add(keyword)
        
        return list(keywords)[:20]  # Limit to top 20 keywords
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key quantum concepts from text."""
        concepts = [
            "quantum computing", "quantum mechanics", "quantum physics",
            "quantum information", "quantum algorithm", "quantum hardware",
            "quantum software", "quantum application", "quantum theory",
            "quantum cryptography", "quantum machine learning",
            "quantum networking", "quantum error correction"
        ]
        
        found_concepts = [concept for concept in concepts if concept in text]
        return found_concepts[:10]  # Limit to top 10 concepts
    
    def _generate_tags(self, primary: QuantumCategory, secondary: List[QuantumCategory],
                      level: TechnicalLevel, content_type: ContentType) -> List[str]:
        """Generate tags based on categorization results."""
        tags = []
        
        # Add category tags
        tags.append(f"quantum-{primary.value}")
        for cat in secondary:
            tags.append(f"quantum-{cat.value}")
        
        # Add level and type tags
        if level != TechnicalLevel.UNKNOWN:
            tags.append(f"level-{level.value}")
        
        if content_type != ContentType.GENERAL:
            tags.append(f"type-{content_type.value}")
        
        # Add general quantum tag
        tags.append("quantum-computing")
        
        return tags
    
    def _calculate_confidence(self, text: str, categories: List[QuantumCategory],
                            keywords: List[str]) -> float:
        """Calculate confidence score for categorization."""
        # Base confidence from number of categories identified
        category_confidence = min(len(categories) * 0.2, 0.8)
        
        # Keyword density confidence
        keyword_confidence = min(len(keywords) * 0.05, 0.3)
        
        # Text length confidence (longer text generally more reliable)
        text_length_confidence = min(len(text.split()) * 0.001, 0.2)
        
        # Quantum-specific terms confidence
        quantum_terms = ["quantum", "qubit", "superposition", "entanglement"]
        quantum_confidence = sum(0.1 for term in quantum_terms if term in text)
        quantum_confidence = min(quantum_confidence, 0.4)
        
        total_confidence = (
            category_confidence + keyword_confidence +
            text_length_confidence + quantum_confidence
        )
        
        return min(total_confidence, 1.0)


class VideoTagManager:
    """Manages video tags and categorization."""
    
    def __init__(self):
        self.categorizer = QuantumContentCategorizer()
    
    def generate_comprehensive_tags(self, title: str, description: str,
                                  channel_name: str = "") -> Dict:
        """Generate comprehensive tags and categorization for a video."""
        # Get categorization results
        result = self.categorizer.categorize_content(title, description, channel_name)
        
        # Generate additional contextual tags
        contextual_tags = self._generate_contextual_tags(title, description)
        
        # Combine all tags
        all_tags = result.tags + contextual_tags
        
        return {
            "primary_category": result.primary_category.value,
            "secondary_categories": [cat.value for cat in result.secondary_categories],
            "technical_level": result.technical_level.value,
            "content_type": result.content_type.value,
            "confidence_score": result.confidence_score,
            "tags": list(set(all_tags)),  # Remove duplicates
            "keywords": result.keywords,
            "concepts": result.concepts,
            "auto_generated": True,
            "verified": False
        }
    
    def _generate_contextual_tags(self, title: str, description: str) -> List[str]:
        """Generate additional contextual tags."""
        text = f"{title} {description}".lower()
        contextual_tags = []
        
        # Company/Platform tags
        companies = ["ibm", "google", "microsoft", "amazon", "rigetti", "ionq", "xanadu"]
        for company in companies:
            if company in text:
                contextual_tags.append(f"platform-{company}")
        
        # Programming language tags
        languages = ["python", "qiskit", "cirq", "pennylane", "q#", "qasm"]
        for lang in languages:
            if lang in text:
                contextual_tags.append(f"language-{lang}")
        
        # Duration indicators
        if any(word in text for word in ["quick", "short", "brief", "minute"]):
            contextual_tags.append("duration-short")
        elif any(word in text for word in ["deep", "comprehensive", "complete", "full"]):  
            contextual_tags.append("duration-long")
        
        # Audience tags
        if any(word in text for word in ["student", "beginner", "newcomer"]):
            contextual_tags.append("audience-student")
        elif any(word in text for word in ["researcher", "scientist", "academic"]):
            contextual_tags.append("audience-researcher")
        elif any(word in text for word in ["developer", "programmer", "engineer"]):
            contextual_tags.append("audience-developer")
        
        return contextual_tags


# Global instances
categorizer = QuantumContentCategorizer()
tag_manager = VideoTagManager()