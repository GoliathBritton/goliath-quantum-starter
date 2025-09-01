"""
FLYFOX Academy - The Training & Certification Hub for Quantum AI Agents

This package provides comprehensive training, certification, and developer programs
for the NQBA ecosystem, positioning FLYFOX AI as the industry leader in
quantum AI education and adoption.
"""

from .academy_manager import AcademyManager
from .training_engine import TrainingEngine
from .certification_system import CertificationSystem
from .developer_program import DeveloperProgram
from .learning_paths import LearningPath, LearningModule
from .certificates import Certificate, Badge

__all__ = [
    "AcademyManager",
    "TrainingEngine",
    "CertificationSystem",
    "DeveloperProgram",
    "LearningPath",
    "LearningModule",
    "Certificate",
    "Badge",
]

__version__ = "1.0.0"
__author__ = "FLYFOX AI Team"
__description__ = "FLYFOX Academy - Quantum AI Training & Certification Hub"
