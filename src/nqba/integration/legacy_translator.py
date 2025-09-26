"""Legacy System Translator using qdLLM

This module provides translation capabilities between modern APIs and legacy systems,
utilizing qdLLM for reasoning and decision-making in generating mappings.

Key Components:
- LegacyTranslator: Main class for translating between modern and legacy interfaces
- Uses QuantumDiffusionEngine for complex mapping generation
- Integrates with LegacyAnalyzer for input analysis
- Supports bidirectional translation: modern to legacy and legacy to modern
"""

import logging
from typing import Dict, Any, Optional, List

from nqba.integration.legacy_analyzer import LegacyAnalyzer
from qdllm.core.engine import QuantumDiffusionEngine
from qdllm.qnlp.processor import QNLPProcessor  # For additional processing if needed

logger = logging.getLogger(__name__)

class LegacyTranslator:
    """Translator for legacy systems using qdLLM"""
    
    def __init__(self):
        self.analyzer = LegacyAnalyzer()
        self.qd_engine = QuantumDiffusionEngine()
        self.qnlp = QNLPProcessor()
        
        logger.info("Legacy Translator initialized with qdLLM components")
    
    def generate_mapping(self, modern_api: str, legacy_desc: str, direction: str = 'modern_to_legacy', params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate mapping between modern API and legacy system"""
        params = params or {}
        
        # Analyze inputs
        modern_analysis = self.analyzer.analyze_documentation(modern_api)
        legacy_analysis = self.analyzer.analyze_protocol(legacy_desc) if 'protocol' in legacy_desc.lower() else self.analyzer.analyze_code(legacy_desc)
        
        # Prepare prompt for qdLLM
        prompt = f"""
        Create a bidirectional translation mapping:
        Modern: {modern_api}
        Legacy: {legacy_desc}
        Direction: {direction}
        
        Analysis:
        Modern: {modern_analysis}
        Legacy: {legacy_analysis}
        
        Generate:
        1. Translation function code
        2. Mapping dictionary
        3. Conversion rules
        """
        
        # Use qdLLM for generation
        response = self.qd_engine.generate(prompt, temperature=0.7, max_tokens=1024, use_quantum_enhancement=True)
        
        # Process response with QNLP for structure
        structured = self.qnlp.process(response)
        
        return {
            'mapping': structured,
            'raw_response': response,
            'direction': direction,
            'metrics': structured.get('metrics', {})
        }
    
    def translate_call(self, input_call: str, mapping: Dict[str, Any], direction: str = 'modern_to_legacy') -> str:
        """Translate a specific API call using generated mapping"""
        prompt = f"Translate {direction}: {input_call} using mapping: {mapping}"
        return self.qd_engine.infer(prompt)
    
    def validate_translation(self, original: str, translated: str, expected: Optional[str] = None) -> Dict[str, float]:
        """Validate translation accuracy"""
        orig_analysis = self.analyzer.analyze_documentation(original)
        trans_analysis = self.analyzer.analyze_documentation(translated)
        
        similarity = self.analyzer.compare_artifacts(original, translated)
        
        if expected:
            exp_analysis = self.analyzer.analyze_documentation(expected)
            accuracy = self.analyzer.compare_artifacts(translated, expected)['cosine_similarity']
            similarity['accuracy'] = accuracy
        
        return similarity