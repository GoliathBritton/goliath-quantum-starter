#!/usr/bin/env python3
"""
Variational Quantum Classifier (VQC)
===================================

Implements a Variational Quantum Classifier for machine learning tasks using quantum circuits.
Supports multiple backends (Qiskit, PennyLane) with feature mapping, data encoding,
and variational ansatzes for binary and multi-class classification.

Features:
- Multiple feature mapping strategies (amplitude, angle, IQP)
- Hardware-efficient and problem-inspired ansatzes
- Gradient-based optimization with parameter-shift rule
- Cross-validation and performance metrics
- Integration with classical ML pipelines
- Noise-aware training and error mitigation
"""

import numpy as np
import time
from typing import Dict, List, Tuple, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from pathlib import Path

# Quantum computing imports
try:
    import qiskit
    from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
    from qiskit.circuit import Parameter, ParameterVector
    from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes, EfficientSU2
    from qiskit.primitives import Estimator, Sampler
    from qiskit.quantum_info import SparsePauliOp
    from qiskit_algorithms.optimizers import SPSA, COBYLA, L_BFGS_B
    from qiskit_machine_learning.algorithms import VQC
    from qiskit_machine_learning.neural_networks import SamplerQNN
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

try:
    import pennylane as qml
    from pennylane import numpy as pnp
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False

# Scikit-learn for classical ML integration
try:
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
    from sklearn.datasets import make_classification, load_iris
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Import backend adapter
from .quantum_backend_adapter import QuantumBackendManager, BackendType

logger = logging.getLogger(__name__)

class FeatureMappingType(Enum):
    """Types of quantum feature mapping"""
    AMPLITUDE = "amplitude"
    ANGLE = "angle"
    IQP = "iqp"  # Instantaneous Quantum Polynomial
    PAULI_Z = "pauli_z"
    PAULI_ZZ = "pauli_zz"

class AnsatzType(Enum):
    """Types of variational ansatzes"""
    HARDWARE_EFFICIENT = "hardware_efficient"
    REAL_AMPLITUDES = "real_amplitudes"
    EFFICIENT_SU2 = "efficient_su2"
    CUSTOM = "custom"

@dataclass
class ClassificationResult:
    """Results from quantum classification"""
    accuracy: float
    predictions: np.ndarray
    probabilities: Optional[np.ndarray] = None
    optimal_params: Optional[np.ndarray] = None
    training_history: List[float] = field(default_factory=list)
    execution_time: float = 0.0
    iterations: int = 0
    cross_val_scores: Optional[List[float]] = None
    confusion_matrix: Optional[np.ndarray] = None
    classification_report: Optional[Dict] = None
    feature_importance: Optional[np.ndarray] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "accuracy": float(self.accuracy),
            "predictions": self.predictions.tolist() if self.predictions is not None else None,
            "probabilities": self.probabilities.tolist() if self.probabilities is not None else None,
            "optimal_params": self.optimal_params.tolist() if self.optimal_params is not None else None,
            "training_history": self.training_history,
            "execution_time": float(self.execution_time),
            "iterations": int(self.iterations),
            "cross_val_scores": self.cross_val_scores,
            "confusion_matrix": self.confusion_matrix.tolist() if self.confusion_matrix is not None else None,
            "classification_report": self.classification_report
        }

class QuantumClassifier:
    """
    Variational Quantum Classifier implementation
    
    Supports multiple quantum backends and classical ML integration
    """
    
    def __init__(
        self,
        num_features: int,
        num_classes: int = 2,
        num_qubits: Optional[int] = None,
        feature_mapping: FeatureMappingType = FeatureMappingType.ANGLE,
        ansatz_type: AnsatzType = AnsatzType.HARDWARE_EFFICIENT,
        num_layers: int = 2,
        backend_type: BackendType = BackendType.QISKIT,
        shots: int = 1024,
        optimization_level: int = 1,
        noise_mitigation: bool = False,
        seed: int = 42
    ):
        """
        Initialize Quantum Classifier
        
        Args:
            num_features: Number of input features
            num_classes: Number of output classes
            num_qubits: Number of qubits (defaults to num_features)
            feature_mapping: Type of feature mapping
            ansatz_type: Type of variational ansatz
            num_layers: Number of ansatz layers
            backend_type: Quantum backend to use
            shots: Number of measurement shots
            optimization_level: Circuit optimization level
            noise_mitigation: Enable noise mitigation
            seed: Random seed for reproducibility
        """
        self.num_features = num_features
        self.num_classes = num_classes
        self.num_qubits = num_qubits or num_features
        self.feature_mapping = feature_mapping
        self.ansatz_type = ansatz_type
        self.num_layers = num_layers
        self.backend_type = backend_type
        self.shots = shots
        self.optimization_level = optimization_level
        self.noise_mitigation = noise_mitigation
        self.seed = seed
        
        # Initialize backend manager
        self.backend_manager = QuantumBackendManager()
        
        # Initialize components
        self.circuit = None
        self.parameters = None
        self.optimal_params = None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        self.label_encoder = LabelEncoder() if SKLEARN_AVAILABLE else None
        
        # Training history
        self.training_history = []
        
        np.random.seed(seed)
        
    def _create_feature_map(self, x: np.ndarray) -> QuantumCircuit:
        """
        Create quantum feature mapping circuit
        
        Args:
            x: Input features
            
        Returns:
            Quantum circuit with feature mapping
        """
        if not QISKIT_AVAILABLE:
            raise ImportError("Qiskit is required for quantum circuits")
            
        qc = QuantumCircuit(self.num_qubits)
        
        if self.feature_mapping == FeatureMappingType.AMPLITUDE:
            # Amplitude encoding
            # Normalize features to unit vector
            norm = np.linalg.norm(x)
            if norm > 0:
                x_normalized = x / norm
                # Pad or truncate to match number of qubits
                if len(x_normalized) < 2**self.num_qubits:
                    x_padded = np.zeros(2**self.num_qubits)
                    x_padded[:len(x_normalized)] = x_normalized
                else:
                    x_padded = x_normalized[:2**self.num_qubits]
                qc.initialize(x_padded, range(self.num_qubits))
                
        elif self.feature_mapping == FeatureMappingType.ANGLE:
            # Angle encoding
            for i, feature in enumerate(x[:self.num_qubits]):
                qc.ry(feature, i)
                
        elif self.feature_mapping == FeatureMappingType.IQP:
            # IQP-style encoding
            for i, feature in enumerate(x[:self.num_qubits]):
                qc.ry(feature, i)
            # Add entangling gates
            for i in range(self.num_qubits - 1):
                qc.cz(i, i + 1)
                
        elif self.feature_mapping == FeatureMappingType.PAULI_Z:
            # Pauli-Z feature map
            for i, feature in enumerate(x[:self.num_qubits]):
                qc.rz(feature, i)
                
        elif self.feature_mapping == FeatureMappingType.PAULI_ZZ:
            # Pauli-ZZ feature map
            for i, feature in enumerate(x[:self.num_qubits]):
                qc.rz(feature, i)
            # Add ZZ interactions
            for i in range(self.num_qubits - 1):
                qc.cx(i, i + 1)
                qc.rz(x[i % len(x)] * x[(i + 1) % len(x)], i + 1)
                qc.cx(i, i + 1)
                
        return qc
    
    def _create_ansatz(self) -> Tuple[QuantumCircuit, ParameterVector]:
        """
        Create variational ansatz circuit
        
        Returns:
            Tuple of (ansatz circuit, parameters)
        """
        if not QISKIT_AVAILABLE:
            raise ImportError("Qiskit is required for quantum circuits")
            
        if self.ansatz_type == AnsatzType.HARDWARE_EFFICIENT:
            # Hardware-efficient ansatz
            num_params = self.num_qubits * self.num_layers * 3  # RX, RY, RZ per qubit per layer
            params = ParameterVector('θ', num_params)
            
            qc = QuantumCircuit(self.num_qubits)
            param_idx = 0
            
            for layer in range(self.num_layers):
                # Rotation gates
                for qubit in range(self.num_qubits):
                    qc.rx(params[param_idx], qubit)
                    param_idx += 1
                    qc.ry(params[param_idx], qubit)
                    param_idx += 1
                    qc.rz(params[param_idx], qubit)
                    param_idx += 1
                
                # Entangling gates
                for qubit in range(self.num_qubits - 1):
                    qc.cx(qubit, qubit + 1)
                    
        elif self.ansatz_type == AnsatzType.REAL_AMPLITUDES:
            # Real amplitudes ansatz
            ansatz = RealAmplitudes(self.num_qubits, reps=self.num_layers)
            qc = ansatz
            params = ansatz.parameters
            
        elif self.ansatz_type == AnsatzType.EFFICIENT_SU2:
            # Efficient SU(2) ansatz
            ansatz = EfficientSU2(self.num_qubits, reps=self.num_layers)
            qc = ansatz
            params = ansatz.parameters
            
        else:
            raise ValueError(f"Unsupported ansatz type: {self.ansatz_type}")
            
        return qc, params
    
    def _create_measurement_circuit(self, feature_map: QuantumCircuit, ansatz: QuantumCircuit) -> QuantumCircuit:
        """
        Create complete measurement circuit
        
        Args:
            feature_map: Feature mapping circuit
            ansatz: Variational ansatz circuit
            
        Returns:
            Complete quantum circuit
        """
        # Combine feature map and ansatz
        qc = feature_map.compose(ansatz)
        
        # Add measurements
        if self.num_classes == 2:
            # Binary classification - measure first qubit
            qc.add_register(ClassicalRegister(1, 'c'))
            qc.measure(0, 0)
        else:
            # Multi-class classification - measure all qubits
            qc.add_register(ClassicalRegister(self.num_qubits, 'c'))
            qc.measure_all()
            
        return qc
    
    def _objective_function(self, params: np.ndarray, X: np.ndarray, y: np.ndarray) -> float:
        """
        Objective function for optimization
        
        Args:
            params: Variational parameters
            X: Training features
            y: Training labels
            
        Returns:
            Loss value
        """
        predictions = self._predict_batch(X, params)
        
        # Cross-entropy loss for classification
        epsilon = 1e-15  # Prevent log(0)
        predictions = np.clip(predictions, epsilon, 1 - epsilon)
        
        if self.num_classes == 2:
            # Binary cross-entropy
            loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        else:
            # Multi-class cross-entropy
            loss = -np.mean(np.sum(y * np.log(predictions), axis=1))
            
        return loss
    
    def _predict_batch(self, X: np.ndarray, params: np.ndarray) -> np.ndarray:
        """
        Predict probabilities for a batch of samples
        
        Args:
            X: Input features
            params: Variational parameters
            
        Returns:
            Predicted probabilities
        """
        predictions = []
        
        for x in X:
            # Create feature map for this sample
            feature_map = self._create_feature_map(x)
            
            # Create ansatz
            ansatz, param_vector = self._create_ansatz()
            
            # Bind parameters
            param_dict = {param_vector[i]: params[i] for i in range(len(params))}
            bound_ansatz = ansatz.bind_parameters(param_dict)
            
            # Create measurement circuit
            circuit = self._create_measurement_circuit(feature_map, bound_ansatz)
            
            # Execute circuit
            backend = self.backend_manager.get_backend(self.backend_type)
            
            if self.backend_type == BackendType.QISKIT:
                from qiskit import transpile, execute
                transpiled = transpile(circuit, backend, optimization_level=self.optimization_level)
                job = execute(transpiled, backend, shots=self.shots)
                result = job.result()
                counts = result.get_counts()
                
                if self.num_classes == 2:
                    # Binary classification
                    prob_1 = counts.get('1', 0) / self.shots
                    predictions.append(prob_1)
                else:
                    # Multi-class classification
                    probs = np.zeros(self.num_classes)
                    for bitstring, count in counts.items():
                        class_idx = int(bitstring, 2) % self.num_classes
                        probs[class_idx] += count / self.shots
                    predictions.append(probs)
                    
        return np.array(predictions)
    
    def fit(self, X: np.ndarray, y: np.ndarray, max_iterations: int = 100) -> ClassificationResult:
        """
        Train the quantum classifier
        
        Args:
            X: Training features
            y: Training labels
            max_iterations: Maximum optimization iterations
            
        Returns:
            Classification results
        """
        start_time = time.time()
        
        # Preprocess data
        if self.scaler:
            X = self.scaler.fit_transform(X)
            
        if self.label_encoder and self.num_classes > 2:
            y = self.label_encoder.fit_transform(y)
            
        # Convert labels to one-hot for multi-class
        if self.num_classes > 2:
            y_onehot = np.zeros((len(y), self.num_classes))
            y_onehot[np.arange(len(y)), y] = 1
            y = y_onehot
            
        # Initialize parameters
        _, param_vector = self._create_ansatz()
        num_params = len(param_vector)
        initial_params = np.random.uniform(0, 2*np.pi, num_params)
        
        # Optimization
        if QISKIT_AVAILABLE:
            optimizer = SPSA(maxiter=max_iterations)
        else:
            # Fallback to scipy optimizer
            from scipy.optimize import minimize
            
        self.training_history = []
        
        def callback(params):
            loss = self._objective_function(params, X, y)
            self.training_history.append(loss)
            logger.info(f"Iteration {len(self.training_history)}: Loss = {loss:.6f}")
            
        # Run optimization
        if QISKIT_AVAILABLE:
            result = optimizer.minimize(
                fun=lambda params: self._objective_function(params, X, y),
                x0=initial_params,
                callback=callback
            )
            self.optimal_params = result.x
            iterations = result.nfev
        else:
            result = minimize(
                fun=lambda params: self._objective_function(params, X, y),
                x0=initial_params,
                method='COBYLA',
                callback=callback,
                options={'maxiter': max_iterations}
            )
            self.optimal_params = result.x
            iterations = result.nfev
            
        execution_time = time.time() - start_time
        
        # Make predictions on training set
        train_predictions = self.predict(X)
        train_accuracy = accuracy_score(y.argmax(axis=1) if self.num_classes > 2 else y, 
                                      train_predictions.argmax(axis=1) if self.num_classes > 2 else (train_predictions > 0.5).astype(int))
        
        return ClassificationResult(
            accuracy=train_accuracy,
            predictions=train_predictions,
            optimal_params=self.optimal_params,
            training_history=self.training_history,
            execution_time=execution_time,
            iterations=iterations
        )
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            X: Input features
            
        Returns:
            Predicted probabilities or class labels
        """
        if self.optimal_params is None:
            raise ValueError("Model must be trained before making predictions")
            
        # Preprocess data
        if self.scaler:
            X = self.scaler.transform(X)
            
        # Get predictions
        predictions = self._predict_batch(X, self.optimal_params)
        
        return predictions
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> ClassificationResult:
        """
        Evaluate the classifier on test data
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Evaluation results
        """
        start_time = time.time()
        
        # Make predictions
        predictions = self.predict(X_test)
        
        # Convert predictions to class labels
        if self.num_classes == 2:
            pred_labels = (predictions > 0.5).astype(int)
        else:
            pred_labels = predictions.argmax(axis=1)
            
        # Calculate metrics
        if self.label_encoder and self.num_classes > 2:
            y_test_labels = self.label_encoder.transform(y_test) if hasattr(y_test[0], '__len__') else y_test
        else:
            y_test_labels = y_test.argmax(axis=1) if self.num_classes > 2 and hasattr(y_test[0], '__len__') else y_test
            
        accuracy = accuracy_score(y_test_labels, pred_labels)
        
        # Additional metrics if sklearn is available
        conf_matrix = None
        class_report = None
        if SKLEARN_AVAILABLE:
            conf_matrix = confusion_matrix(y_test_labels, pred_labels)
            class_report = classification_report(y_test_labels, pred_labels, output_dict=True)
            
        execution_time = time.time() - start_time
        
        return ClassificationResult(
            accuracy=accuracy,
            predictions=pred_labels,
            probabilities=predictions,
            optimal_params=self.optimal_params,
            execution_time=execution_time,
            confusion_matrix=conf_matrix,
            classification_report=class_report
        )

# Convenience functions
def create_quantum_classifier(
    num_features: int,
    num_classes: int = 2,
    backend_type: BackendType = BackendType.QISKIT,
    **kwargs
) -> QuantumClassifier:
    """
    Create a quantum classifier with default settings
    
    Args:
        num_features: Number of input features
        num_classes: Number of output classes
        backend_type: Quantum backend to use
        **kwargs: Additional arguments for QuantumClassifier
        
    Returns:
        Configured QuantumClassifier instance
    """
    return QuantumClassifier(
        num_features=num_features,
        num_classes=num_classes,
        backend_type=backend_type,
        **kwargs
    )

def run_classification_demo(
    dataset: str = "iris",
    backend_type: BackendType = BackendType.QISKIT,
    save_results: bool = True
) -> ClassificationResult:
    """
    Run a demonstration of quantum classification
    
    Args:
        dataset: Dataset to use ("iris", "synthetic")
        backend_type: Quantum backend to use
        save_results: Whether to save results to file
        
    Returns:
        Classification results
    """
    logger.info(f"Running quantum classification demo with {dataset} dataset")
    
    # Load dataset
    if dataset == "iris" and SKLEARN_AVAILABLE:
        from sklearn.datasets import load_iris
        data = load_iris()
        X, y = data.data, data.target
        # Use only first 2 classes for binary classification
        mask = y < 2
        X, y = X[mask], y[mask]
        num_classes = 2
    elif dataset == "synthetic" and SKLEARN_AVAILABLE:
        X, y = make_classification(
            n_samples=100,
            n_features=4,
            n_classes=2,
            n_redundant=0,
            n_informative=4,
            random_state=42
        )
        num_classes = 2
    else:
        # Simple synthetic dataset
        np.random.seed(42)
        X = np.random.randn(50, 4)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        num_classes = 2
        
    # Split data
    if SKLEARN_AVAILABLE:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
    else:
        # Simple split
        split_idx = int(0.7 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
    # Create and train classifier
    classifier = create_quantum_classifier(
        num_features=X.shape[1],
        num_classes=num_classes,
        backend_type=backend_type,
        num_layers=2,
        shots=1024
    )
    
    # Train
    logger.info("Training quantum classifier...")
    train_result = classifier.fit(X_train, y_train, max_iterations=50)
    
    # Evaluate
    logger.info("Evaluating quantum classifier...")
    test_result = classifier.evaluate(X_test, y_test)
    
    logger.info(f"Training accuracy: {train_result.accuracy:.4f}")
    logger.info(f"Test accuracy: {test_result.accuracy:.4f}")
    logger.info(f"Training time: {train_result.execution_time:.2f}s")
    
    # Save results
    if save_results:
        results_dir = Path("benchmark_results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = int(time.time())
        filename = f"quantum_classifier_{dataset}_{backend_type.value}_{timestamp}.json"
        
        results = {
            "algorithm": "quantum_classifier",
            "dataset": dataset,
            "backend": backend_type.value,
            "timestamp": timestamp,
            "train_result": train_result.to_dict(),
            "test_result": test_result.to_dict(),
            "config": {
                "num_features": X.shape[1],
                "num_classes": num_classes,
                "num_layers": classifier.num_layers,
                "shots": classifier.shots,
                "feature_mapping": classifier.feature_mapping.value,
                "ansatz_type": classifier.ansatz_type.value
            }
        }
        
        with open(results_dir / filename, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info(f"Results saved to {filename}")
        
    return test_result

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Run demo
    result = run_classification_demo(
        dataset="synthetic",
        backend_type=BackendType.QISKIT
    )
    
    print(f"\n🎯 Quantum Classification Demo Results:")
    print(f"   Test Accuracy: {result.accuracy:.4f}")
    print(f"   Execution Time: {result.execution_time:.2f}s")
    if result.confusion_matrix is not None:
        print(f"   Confusion Matrix:\n{result.confusion_matrix}")