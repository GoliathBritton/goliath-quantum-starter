import unittest
import sys
sys.path.append('src')

from nqba_stack.security.ai_safety_governance import AISafetyGovernance
from nqba_stack.training.federated_learning_engine import FederatedLearningEngine
from nqba_stack.core.enhanced_quantum_runtime import EnhancedQuantumRuntime
from nqba_stack.observability.quantum_observability_suite import QuantumObservabilitySuite
from nqba_stack.algorithms.ml_algorithms.quantum_ml_pipeline import QuantumMLPipeline
from nqba_stack.blockchain.blockchain_security_layer import BlockchainSecurityLayer
# from nqba_stack.core.quantum_digital_agents import AutonomousAIAgents
from nqba_stack.security.quantum_secure_communication import QuantumSecureCommunication
from nqba_stack.benchmarks.enhanced_benchmarks import EnhancedBenchmarks

class TestAdvancedSystems(unittest.TestCase):
    def test_ai_safety_governance(self):
        instance = AISafetyGovernance()
        self.assertIsNotNone(instance)
        # Add more assertions if needed

    def test_federated_learning_engine(self):
        instance = FederatedLearningEngine()
        self.assertIsNotNone(instance)

    def test_enhanced_quantum_runtime(self):
        instance = EnhancedQuantumRuntime()
        self.assertIsNotNone(instance)

    def test_quantum_observability_suite(self):
        instance = QuantumObservabilitySuite()
        self.assertIsNotNone(instance)

    def test_quantum_ml_pipeline(self):
        instance = QuantumMLPipeline()
        self.assertIsNotNone(instance)

    def test_blockchain_security_layer(self):
        instance = BlockchainSecurityLayer()
        self.assertIsNotNone(instance)

    # def test_autonomous_ai_agents(self):
    #     instance = AutonomousAIAgents()
    #     self.assertIsNotNone(instance)

    def test_quantum_secure_communication(self):
        instance = QuantumSecureCommunication()
        self.assertIsNotNone(instance)

    def test_enhanced_benchmarks(self):
        instance = EnhancedBenchmarks()
        self.assertIsNotNone(instance)

if __name__ == '__main__':
    unittest.main()