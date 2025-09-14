// Quantum Types for Goliath Quantum Starter

export interface QuantumCircuit {
  id: string;
  name: string;
  gates: QuantumGate[];
  qubits: number;
  depth: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface QuantumGate {
  id: string;
  type: 'H' | 'X' | 'Y' | 'Z' | 'CNOT' | 'CZ' | 'RX' | 'RY' | 'RZ' | 'T' | 'S';
  qubits: number[];
  parameters?: number[];
  matrix?: number[][];
}

export interface QuantumState {
  id: string;
  amplitudes: Complex[];
  qubits: number;
  entangled: boolean;
  measurementProbabilities: number[];
}

export interface Complex {
  real: number;
  imaginary: number;
}

export interface QuantumMeasurement {
  qubit: number;
  result: 0 | 1;
  probability: number;
  timestamp: Date;
}

export interface QuantumAlgorithm {
  id: string;
  name: string;
  description: string;
  circuit: QuantumCircuit;
  expectedOutput: string;
  complexity: 'low' | 'medium' | 'high';
}

export interface QuantumOptimizationResult {
  solution: number[];
  energy: number;
  iterations: number;
  convergenceTime: number;
  success: boolean;
}

export interface QUBOMatrix {
  size: number;
  matrix: number[][];
  variables: string[];
  objective: string;
}

export type QuantumBackend = 'simulator' | 'dynex' | 'ibm' | 'google' | 'rigetti';

export interface QuantumJob {
  id: string;
  circuit: QuantumCircuit;
  backend: QuantumBackend;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: QuantumState;
  error?: string;
  submittedAt: Date;
  completedAt?: Date;
}