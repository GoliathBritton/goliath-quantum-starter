import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert,
  Dimensions,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  List,
  Divider,
  Surface,
  Text,
  ProgressBar,
  FAB,
  Badge,
  Switch,
  IconButton,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
// import { LineChart, BarChart } from 'react-native-chart-kit'; // Removed for compatibility

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface GhostNeuroQScreenProps {
  navigation: any;
}

interface NeuroQuantumNode {
  id: string;
  name: string;
  type: 'input' | 'hidden' | 'output' | 'quantum' | 'classical';
  layer: number;
  position: { x: number; y: number };
  activation: number;
  quantumState: {
    amplitude: number;
    phase: number;
    entanglement: number;
    coherence: number;
  };
  connections: string[];
  parameters: {
    weights: number[];
    bias: number;
    learningRate: number;
  };
  isActive: boolean;
  lastUpdate: string;
}

interface QuantumCircuit {
  id: string;
  name: string;
  description: string;
  qubits: number;
  depth: number;
  gates: {
    type: 'H' | 'X' | 'Y' | 'Z' | 'CNOT' | 'RX' | 'RY' | 'RZ' | 'SWAP';
    target: number[];
    control?: number;
    angle?: number;
    position: number;
  }[];
  fidelity: number;
  executionTime: number;
  errorRate: number;
  status: 'idle' | 'running' | 'completed' | 'error';
  results?: {
    measurements: number[];
    probabilities: number[];
    entanglementEntropy: number;
  };
  createdAt: string;
}

interface TrainingSession {
  id: string;
  name: string;
  modelType: 'QNN' | 'QCNN' | 'VQE' | 'QAOA' | 'Hybrid';
  dataset: string;
  epochs: number;
  currentEpoch: number;
  batchSize: number;
  learningRate: number;
  status: 'preparing' | 'training' | 'paused' | 'completed' | 'failed';
  metrics: {
    loss: number[];
    accuracy: number[];
    quantumFidelity: number[];
    classicalAccuracy: number[];
  };
  hyperparameters: {
    optimizer: string;
    quantumLayers: number;
    classicalLayers: number;
    entanglementPattern: string;
  };
  startTime: string;
  estimatedCompletion?: string;
  hardware: {
    backend: string;
    qubits: number;
    shots: number;
    noiseModel: boolean;
  };
}

const GhostNeuroQScreen: React.FC<GhostNeuroQScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [nodes, setNodes] = useState<NeuroQuantumNode[]>([]);
  const [circuits, setCircuits] = useState<QuantumCircuit[]>([]);
  const [trainingSessions, setTrainingSessions] = useState<TrainingSession[]>([]);
  const [activeTab, setActiveTab] = useState<'network' | 'circuits' | 'training'>('network');
  const [systemMetrics, setSystemMetrics] = useState({
    quantumCoherence: 0.89,
    neuralActivation: 0.76,
    entanglementStrength: 0.82,
    learningEfficiency: 0.91,
    quantumAdvantage: 0.73
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock nodes data
      const mockNodes: NeuroQuantumNode[] = [
        {
          id: '1',
          name: 'Input Qubit 1',
          type: 'quantum',
          layer: 0,
          position: { x: 50, y: 100 },
          activation: 0.87,
          quantumState: {
            amplitude: 0.92,
            phase: 1.23,
            entanglement: 0.76,
            coherence: 0.89
          },
          connections: ['3', '4'],
          parameters: {
            weights: [0.45, 0.67, -0.23],
            bias: 0.12,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date().toISOString()
        },
        {
          id: '2',
          name: 'Input Qubit 2',
          type: 'quantum',
          layer: 0,
          position: { x: 50, y: 200 },
          activation: 0.64,
          quantumState: {
            amplitude: 0.78,
            phase: 2.45,
            entanglement: 0.82,
            coherence: 0.91
          },
          connections: ['3', '5'],
          parameters: {
            weights: [0.32, -0.18, 0.56],
            bias: -0.08,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date(Date.now() - 300000).toISOString()
        },
        {
          id: '3',
          name: 'Hidden Quantum Layer',
          type: 'quantum',
          layer: 1,
          position: { x: 150, y: 150 },
          activation: 0.73,
          quantumState: {
            amplitude: 0.85,
            phase: 0.67,
            entanglement: 0.94,
            coherence: 0.87
          },
          connections: ['6'],
          parameters: {
            weights: [0.78, 0.23, -0.45, 0.12],
            bias: 0.34,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date(Date.now() - 600000).toISOString()
        },
        {
          id: '4',
          name: 'Classical Hidden 1',
          type: 'classical',
          layer: 1,
          position: { x: 150, y: 100 },
          activation: 0.82,
          quantumState: {
            amplitude: 0,
            phase: 0,
            entanglement: 0,
            coherence: 0
          },
          connections: ['6'],
          parameters: {
            weights: [0.56, -0.34, 0.78],
            bias: 0.23,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date(Date.now() - 900000).toISOString()
        },
        {
          id: '5',
          name: 'Classical Hidden 2',
          type: 'classical',
          layer: 1,
          position: { x: 150, y: 200 },
          activation: 0.69,
          quantumState: {
            amplitude: 0,
            phase: 0,
            entanglement: 0,
            coherence: 0
          },
          connections: ['6'],
          parameters: {
            weights: [0.12, 0.89, -0.67],
            bias: -0.15,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date(Date.now() - 1200000).toISOString()
        },
        {
          id: '6',
          name: 'Output Node',
          type: 'output',
          layer: 2,
          position: { x: 250, y: 150 },
          activation: 0.91,
          quantumState: {
            amplitude: 0.96,
            phase: 3.14,
            entanglement: 0.88,
            coherence: 0.93
          },
          connections: [],
          parameters: {
            weights: [0.67, 0.45, 0.23, -0.12],
            bias: 0.08,
            learningRate: 0.001
          },
          isActive: true,
          lastUpdate: new Date(Date.now() - 150000).toISOString()
        }
      ];
      
      // Mock circuits data
      const mockCircuits: QuantumCircuit[] = [
        {
          id: '1',
          name: 'Variational Quantum Classifier',
          description: 'Quantum circuit for binary classification with variational parameters',
          qubits: 4,
          depth: 8,
          gates: [
            { type: 'H', target: [0], position: 0 },
            { type: 'H', target: [1], position: 0 },
            { type: 'CNOT', target: [1], control: 0, position: 1 },
            { type: 'RY', target: [0], angle: 1.23, position: 2 },
            { type: 'RY', target: [1], angle: 0.67, position: 2 },
            { type: 'CNOT', target: [1], control: 0, position: 3 },
            { type: 'H', target: [2], position: 4 },
            { type: 'CNOT', target: [2], control: 1, position: 5 }
          ],
          fidelity: 0.94,
          executionTime: 2.3,
          errorRate: 0.02,
          status: 'completed',
          results: {
            measurements: [1, 0, 1, 1, 0, 1, 0, 0],
            probabilities: [0.23, 0.77, 0.15, 0.85],
            entanglementEntropy: 1.45
          },
          createdAt: new Date(Date.now() - 3600000).toISOString()
        },
        {
          id: '2',
          name: 'Quantum Approximate Optimization',
          description: 'QAOA circuit for combinatorial optimization problems',
          qubits: 6,
          depth: 12,
          gates: [
            { type: 'H', target: [0, 1, 2, 3, 4, 5], position: 0 },
            { type: 'RZ', target: [0], angle: 0.45, position: 1 },
            { type: 'RZ', target: [1], angle: 0.67, position: 1 },
            { type: 'CNOT', target: [1], control: 0, position: 2 },
            { type: 'CNOT', target: [2], control: 1, position: 2 },
            { type: 'RX', target: [0, 1, 2, 3, 4, 5], angle: 1.23, position: 3 }
          ],
          fidelity: 0.87,
          executionTime: 4.7,
          errorRate: 0.05,
          status: 'running',
          createdAt: new Date(Date.now() - 1800000).toISOString()
        },
        {
          id: '3',
          name: 'Quantum Convolutional Layer',
          description: 'Quantum convolution for image processing applications',
          qubits: 8,
          depth: 16,
          gates: [
            { type: 'H', target: [0, 1, 2, 3], position: 0 },
            { type: 'CNOT', target: [1], control: 0, position: 1 },
            { type: 'CNOT', target: [2], control: 1, position: 1 },
            { type: 'CNOT', target: [3], control: 2, position: 1 },
            { type: 'RY', target: [0, 1, 2, 3], angle: 0.78, position: 2 }
          ],
          fidelity: 0.91,
          executionTime: 6.2,
          errorRate: 0.03,
          status: 'idle',
          createdAt: new Date(Date.now() - 7200000).toISOString()
        }
      ];
      
      // Mock training sessions data
      const mockTrainingSessions: TrainingSession[] = [
        {
          id: '1',
          name: 'MNIST Quantum Classification',
          modelType: 'QCNN',
          dataset: 'MNIST Digits',
          epochs: 100,
          currentEpoch: 67,
          batchSize: 32,
          learningRate: 0.001,
          status: 'training',
          metrics: {
            loss: [0.89, 0.76, 0.65, 0.58, 0.52, 0.48, 0.45],
            accuracy: [0.23, 0.45, 0.67, 0.78, 0.82, 0.85, 0.87],
            quantumFidelity: [0.92, 0.93, 0.94, 0.95, 0.94, 0.95, 0.96],
            classicalAccuracy: [0.21, 0.43, 0.64, 0.75, 0.79, 0.82, 0.84]
          },
          hyperparameters: {
            optimizer: 'Adam',
            quantumLayers: 4,
            classicalLayers: 2,
            entanglementPattern: 'circular'
          },
          startTime: new Date(Date.now() - 14400000).toISOString(),
          estimatedCompletion: new Date(Date.now() + 7200000).toISOString(),
          hardware: {
            backend: 'qasm_simulator',
            qubits: 16,
            shots: 1024,
            noiseModel: true
          }
        },
        {
          id: '2',
          name: 'Quantum Portfolio Optimization',
          modelType: 'QAOA',
          dataset: 'Financial Markets',
          epochs: 50,
          currentEpoch: 50,
          batchSize: 16,
          learningRate: 0.01,
          status: 'completed',
          metrics: {
            loss: [1.23, 0.98, 0.76, 0.65, 0.58, 0.52, 0.48],
            accuracy: [0.34, 0.56, 0.67, 0.78, 0.82, 0.86, 0.89],
            quantumFidelity: [0.87, 0.89, 0.91, 0.93, 0.94, 0.95, 0.96],
            classicalAccuracy: [0.32, 0.54, 0.64, 0.75, 0.79, 0.83, 0.86]
          },
          hyperparameters: {
            optimizer: 'COBYLA',
            quantumLayers: 6,
            classicalLayers: 1,
            entanglementPattern: 'linear'
          },
          startTime: new Date(Date.now() - 86400000).toISOString(),
          hardware: {
            backend: 'ibmq_qasm_simulator',
            qubits: 12,
            shots: 2048,
            noiseModel: false
          }
        },
        {
          id: '3',
          name: 'Quantum Drug Discovery',
          modelType: 'VQE',
          dataset: 'Molecular Structures',
          epochs: 200,
          currentEpoch: 23,
          batchSize: 8,
          learningRate: 0.005,
          status: 'training',
          metrics: {
            loss: [2.45, 2.12, 1.89, 1.67, 1.45, 1.23, 1.08],
            accuracy: [0.12, 0.23, 0.34, 0.45, 0.56, 0.67, 0.72],
            quantumFidelity: [0.78, 0.82, 0.85, 0.87, 0.89, 0.91, 0.93],
            classicalAccuracy: [0.10, 0.21, 0.32, 0.43, 0.54, 0.64, 0.69]
          },
          hyperparameters: {
            optimizer: 'SPSA',
            quantumLayers: 8,
            classicalLayers: 3,
            entanglementPattern: 'full'
          },
          startTime: new Date(Date.now() - 7200000).toISOString(),
          estimatedCompletion: new Date(Date.now() + 28800000).toISOString(),
          hardware: {
            backend: 'ibmq_montreal',
            qubits: 27,
            shots: 4096,
            noiseModel: true
          }
        }
      ];
      
      setNodes(mockNodes);
      setCircuits(mockCircuits);
      setTrainingSessions(mockTrainingSessions);
      
    } catch (error) {
      console.error('Load data error:', error);
      Alert.alert('Error', 'Failed to load Ghost NeuroQ data');
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'running':
      case 'training':
      case 'completed':
        return theme.colors.primary;
      case 'preparing':
      case 'paused':
      case 'idle':
        return theme.colors.tertiary;
      case 'failed':
      case 'error':
        return theme.colors.error;
      default:
        return theme.colors.outline;
    }
  };

  const getNodeTypeColor = (type: NeuroQuantumNode['type']) => {
    switch (type) {
      case 'quantum':
        return '#9C27B0';
      case 'classical':
        return '#2196F3';
      case 'input':
        return '#4CAF50';
      case 'hidden':
        return '#FF9800';
      case 'output':
        return '#F44336';
      default:
        return theme.colors.outline;
    }
  };

  const formatNumber = (value: number, decimals: number = 3) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const handleNodePress = (node: NeuroQuantumNode) => {
    navigation.navigate('NodeDetails', { nodeId: node.id });
  };

  const handleCircuitPress = (circuit: QuantumCircuit) => {
    navigation.navigate('CircuitDetails', { circuitId: circuit.id });
  };

  const handleTrainingPress = (session: TrainingSession) => {
    navigation.navigate('TrainingDetails', { sessionId: session.id });
  };

  const handleNodeToggle = (nodeId: string) => {
    setNodes(prev => prev.map(node => 
      node.id === nodeId ? { ...node, isActive: !node.isActive } : node
    ));
  };

  const handleCreateCircuit = () => {
    navigation.navigate('CreateCircuit');
  };

  const handleCreateTraining = () => {
    navigation.navigate('CreateTraining');
  };

  if (isLoading && nodes.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading Ghost NeuroQ..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>Ghost NeuroQ</Title>
        <Paragraph style={styles.subtitle}>
          Quantum-Enhanced Neural Networks - Bridging classical and quantum computation
        </Paragraph>
        
        {/* System Metrics */}
        <Card style={styles.metricsCard}>
          <Card.Content>
            <Text style={styles.metricsTitle}>System Metrics</Text>
            <View style={styles.metricsGrid}>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Quantum Coherence</Text>
                <ProgressBar 
                  progress={systemMetrics.quantumCoherence} 
                  color={theme.colors.primary}
                  style={styles.metricBar}
                />
                <Text style={styles.metricValue}>{formatPercentage(systemMetrics.quantumCoherence)}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Neural Activation</Text>
                <ProgressBar 
                  progress={systemMetrics.neuralActivation} 
                  color={theme.colors.secondary}
                  style={styles.metricBar}
                />
                <Text style={styles.metricValue}>{formatPercentage(systemMetrics.neuralActivation)}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Entanglement</Text>
                <ProgressBar 
                  progress={systemMetrics.entanglementStrength} 
                  color={theme.colors.tertiary}
                  style={styles.metricBar}
                />
                <Text style={styles.metricValue}>{formatPercentage(systemMetrics.entanglementStrength)}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Learning Efficiency</Text>
                <ProgressBar 
                  progress={systemMetrics.learningEfficiency} 
                  color='#4CAF50'
                  style={styles.metricBar}
                />
                <Text style={styles.metricValue}>{formatPercentage(systemMetrics.learningEfficiency)}</Text>
              </View>
              <View style={styles.metricItem}>
                <Text style={styles.metricLabel}>Quantum Advantage</Text>
                <ProgressBar 
                  progress={systemMetrics.quantumAdvantage} 
                  color='#FF9800'
                  style={styles.metricBar}
                />
                <Text style={styles.metricValue}>{formatPercentage(systemMetrics.quantumAdvantage)}</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
        
        <View style={styles.tabContainer}>
          <Button
            mode={activeTab === 'network' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('network')}
            style={styles.tabButton}
            compact
          >
            Network
          </Button>
          <Button
            mode={activeTab === 'circuits' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('circuits')}
            style={styles.tabButton}
            compact
          >
            Circuits
          </Button>
          <Button
            mode={activeTab === 'training' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('training')}
            style={styles.tabButton}
            compact
          >
            Training
          </Button>
        </View>
      </Surface>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'network' ? (
          nodes.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="brain" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Neural Network</Title>
                <Paragraph style={styles.emptyText}>
                  Configure your quantum neural network to get started
                </Paragraph>
              </Card.Content>
            </Card>
          ) : (
            nodes.map((node) => (
              <Card 
                key={node.id} 
                style={styles.nodeCard}
                onPress={() => handleNodePress(node)}
              >
                <Card.Content>
                  <View style={styles.nodeHeader}>
                    <View style={styles.nodeInfo}>
                      <View style={styles.nodeTitleRow}>
                        <Icon 
                          name={node.type === 'quantum' ? 'atom' : 'brain'} 
                          size={20} 
                          color={getNodeTypeColor(node.type)} 
                        />
                        <Text style={styles.nodeName}>{node.name}</Text>
                        <Text style={[styles.layerBadge, { backgroundColor: theme.colors.primaryContainer, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, fontSize: 12 }]}>L{node.layer}</Text>
                      </View>
                      <View style={styles.nodeMetaRow}>
                        <Chip 
                          style={[styles.typeChip, { backgroundColor: getNodeTypeColor(node.type) }]}
                          textStyle={{ color: theme.colors.onPrimary }}
                          compact
                        >
                          {node.type}
                        </Chip>
                        <Text style={styles.activationText}>
                          Activation: {formatNumber(node.activation)}
                        </Text>
                      </View>
                    </View>
                    <Switch
                      value={node.isActive}
                      onValueChange={() => handleNodeToggle(node.id)}
                      color={theme.colors.primary}
                    />
                  </View>

                  {node.type === 'quantum' && (
                    <View style={styles.quantumStateContainer}>
                      <Text style={styles.quantumStateTitle}>Quantum State</Text>
                      <View style={styles.quantumMetrics}>
                        <View style={styles.quantumMetricItem}>
                          <Text style={styles.quantumMetricLabel}>Amplitude</Text>
                          <ProgressBar 
                            progress={node.quantumState.amplitude} 
                            color={theme.colors.primary}
                            style={styles.quantumMetricBar}
                          />
                          <Text style={styles.quantumMetricValue}>
                            {formatNumber(node.quantumState.amplitude)}
                          </Text>
                        </View>
                        <View style={styles.quantumMetricItem}>
                          <Text style={styles.quantumMetricLabel}>Phase</Text>
                          <Text style={styles.quantumMetricValue}>
                            {formatNumber(node.quantumState.phase)} rad
                          </Text>
                        </View>
                        <View style={styles.quantumMetricItem}>
                          <Text style={styles.quantumMetricLabel}>Entanglement</Text>
                          <ProgressBar 
                            progress={node.quantumState.entanglement} 
                            color={theme.colors.secondary}
                            style={styles.quantumMetricBar}
                          />
                          <Text style={styles.quantumMetricValue}>
                            {formatNumber(node.quantumState.entanglement)}
                          </Text>
                        </View>
                        <View style={styles.quantumMetricItem}>
                          <Text style={styles.quantumMetricLabel}>Coherence</Text>
                          <ProgressBar 
                            progress={node.quantumState.coherence} 
                            color={theme.colors.tertiary}
                            style={styles.quantumMetricBar}
                          />
                          <Text style={styles.quantumMetricValue}>
                            {formatNumber(node.quantumState.coherence)}
                          </Text>
                        </View>
                      </View>
                    </View>
                  )}

                  <Divider style={styles.divider} />

                  <View style={styles.parametersContainer}>
                    <Text style={styles.parametersTitle}>Parameters</Text>
                    <View style={styles.parametersList}>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Weights:</Text>
                        <Text style={styles.parameterValue}>
                          [{node.parameters.weights.map(w => formatNumber(w, 2)).join(', ')}]
                        </Text>
                      </View>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Bias:</Text>
                        <Text style={styles.parameterValue}>{formatNumber(node.parameters.bias)}</Text>
                      </View>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Learning Rate:</Text>
                        <Text style={styles.parameterValue}>{formatNumber(node.parameters.learningRate, 4)}</Text>
                      </View>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Connections:</Text>
                        <Text style={styles.parameterValue}>{node.connections.length} nodes</Text>
                      </View>
                    </View>
                  </View>

                  <Text style={styles.lastUpdate}>
                    Updated: {new Date(node.lastUpdate).toLocaleString()}
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        ) : activeTab === 'circuits' ? (
          circuits.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="resistor-nodes" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Quantum Circuits</Title>
                <Paragraph style={styles.emptyText}>
                  Create your first quantum circuit to get started
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreateCircuit}
                  style={styles.createButton}
                >
                  Create Circuit
                </Button>
              </Card.Content>
            </Card>
          ) : (
            circuits.map((circuit) => (
              <Card 
                key={circuit.id} 
                style={styles.circuitCard}
                onPress={() => handleCircuitPress(circuit)}
              >
                <Card.Content>
                  <View style={styles.circuitHeader}>
                    <View style={styles.circuitInfo}>
                      <Text style={styles.circuitName}>{circuit.name}</Text>
                      <Text style={styles.circuitDescription}>{circuit.description}</Text>
                    </View>
                    <Chip 
                      style={[styles.statusChip, { backgroundColor: getStatusColor(circuit.status) }]}
                      textStyle={{ color: theme.colors.onPrimary }}
                      compact
                    >
                      {circuit.status}
                    </Chip>
                  </View>

                  <View style={styles.circuitSpecs}>
                    <View style={styles.specItem}>
                      <Icon name="atom" size={16} color={theme.colors.primary} />
                      <Text style={styles.specText}>{circuit.qubits} qubits</Text>
                    </View>
                    <View style={styles.specItem}>
                      <Icon name="layers" size={16} color={theme.colors.secondary} />
                      <Text style={styles.specText}>{circuit.depth} depth</Text>
                    </View>
                    <View style={styles.specItem}>
                      <Icon name="gate" size={16} color={theme.colors.tertiary} />
                      <Text style={styles.specText}>{circuit.gates.length} gates</Text>
                    </View>
                  </View>

                  <View style={styles.circuitMetrics}>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Fidelity</Text>
                      <ProgressBar 
                        progress={circuit.fidelity} 
                        color={theme.colors.primary}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(circuit.fidelity)}</Text>
                    </View>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Error Rate</Text>
                      <ProgressBar 
                        progress={circuit.errorRate} 
                        color={theme.colors.error}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(circuit.errorRate)}</Text>
                    </View>
                  </View>

                  {circuit.results && (
                    <View style={styles.resultsContainer}>
                      <Text style={styles.resultsTitle}>Results</Text>
                      <View style={styles.resultsList}>
                        <View style={styles.resultItem}>
                          <Text style={styles.resultLabel}>Measurements:</Text>
                          <Text style={styles.resultValue}>
                            [{circuit.results.measurements.slice(0, 4).join(', ')}...]
                          </Text>
                        </View>
                        <View style={styles.resultItem}>
                          <Text style={styles.resultLabel}>Entanglement Entropy:</Text>
                          <Text style={styles.resultValue}>
                            {formatNumber(circuit.results.entanglementEntropy)}
                          </Text>
                        </View>
                      </View>
                    </View>
                  )}

                  <Text style={styles.executionTime}>
                    Execution: {formatNumber(circuit.executionTime)} ms
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        ) : (
          trainingSessions.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="school" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Training Sessions</Title>
                <Paragraph style={styles.emptyText}>
                  Start your first quantum machine learning training
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreateTraining}
                  style={styles.createButton}
                >
                  Start Training
                </Button>
              </Card.Content>
            </Card>
          ) : (
            trainingSessions.map((session) => (
              <Card 
                key={session.id} 
                style={styles.trainingCard}
                onPress={() => handleTrainingPress(session)}
              >
                <Card.Content>
                  <View style={styles.trainingHeader}>
                    <View style={styles.trainingInfo}>
                      <Text style={styles.trainingName}>{session.name}</Text>
                      <View style={styles.trainingMeta}>
                        <Chip 
                          style={styles.modelChip}
                          compact
                        >
                          {session.modelType}
                        </Chip>
                        <Text style={styles.datasetText}>{session.dataset}</Text>
                      </View>
                    </View>
                    <Chip 
                      style={[styles.statusChip, { backgroundColor: getStatusColor(session.status) }]}
                      textStyle={{ color: theme.colors.onPrimary }}
                      compact
                    >
                      {session.status}
                    </Chip>
                  </View>

                  {session.status === 'training' && (
                    <View style={styles.progressContainer}>
                      <View style={styles.progressHeader}>
                        <Text style={styles.progressText}>Progress</Text>
                        <Text style={styles.progressPercentage}>
                          {session.currentEpoch}/{session.epochs} epochs
                        </Text>
                      </View>
                      <ProgressBar 
                        progress={session.currentEpoch / session.epochs} 
                        color={theme.colors.primary}
                        style={styles.progressBar}
                      />
                    </View>
                  )}

                  <View style={styles.metricsContainer}>
                    <Text style={styles.metricsTitle}>Current Metrics</Text>
                    <View style={styles.metricsList}>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Loss</Text>
                        <Text style={styles.metricValue}>
                          {formatNumber(session.metrics.loss[session.metrics.loss.length - 1])}
                        </Text>
                      </View>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Accuracy</Text>
                        <Text style={styles.metricValue}>
                          {formatPercentage(session.metrics.accuracy[session.metrics.accuracy.length - 1])}
                        </Text>
                      </View>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Quantum Fidelity</Text>
                        <Text style={styles.metricValue}>
                          {formatPercentage(session.metrics.quantumFidelity[session.metrics.quantumFidelity.length - 1])}
                        </Text>
                      </View>
                    </View>
                  </View>

                  <Divider style={styles.divider} />

                  <View style={styles.hyperparametersContainer}>
                    <Text style={styles.hyperparametersTitle}>Hyperparameters</Text>
                    <View style={styles.hyperparametersList}>
                      <View style={styles.hyperparameterItem}>
                        <Text style={styles.hyperparameterLabel}>Optimizer:</Text>
                        <Text style={styles.hyperparameterValue}>{session.hyperparameters.optimizer}</Text>
                      </View>
                      <View style={styles.hyperparameterItem}>
                        <Text style={styles.hyperparameterLabel}>Quantum Layers:</Text>
                        <Text style={styles.hyperparameterValue}>{session.hyperparameters.quantumLayers}</Text>
                      </View>
                      <View style={styles.hyperparameterItem}>
                        <Text style={styles.hyperparameterLabel}>Learning Rate:</Text>
                        <Text style={styles.hyperparameterValue}>{formatNumber(session.learningRate, 4)}</Text>
                      </View>
                    </View>
                  </View>

                  <View style={styles.hardwareContainer}>
                    <Text style={styles.hardwareTitle}>Hardware</Text>
                    <View style={styles.hardwareSpecs}>
                      <View style={styles.hardwareItem}>
                        <Icon name="chip" size={16} color={theme.colors.primary} />
                        <Text style={styles.hardwareText}>{session.hardware.backend}</Text>
                      </View>
                      <View style={styles.hardwareItem}>
                        <Icon name="atom" size={16} color={theme.colors.secondary} />
                        <Text style={styles.hardwareText}>{session.hardware.qubits} qubits</Text>
                      </View>
                      <View style={styles.hardwareItem}>
                        <Icon name="target" size={16} color={theme.colors.tertiary} />
                        <Text style={styles.hardwareText}>{session.hardware.shots} shots</Text>
                      </View>
                    </View>
                  </View>

                  <Text style={styles.startTime}>
                    Started: {new Date(session.startTime).toLocaleString()}
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        )}
      </ScrollView>

      {(activeTab === 'circuits' || activeTab === 'training') && (
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={activeTab === 'circuits' ? handleCreateCircuit : handleCreateTraining}
          label={activeTab === 'circuits' ? 'New Circuit' : 'New Training'}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    padding: 16,
    elevation: 2,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  subtitle: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 16,
  },
  metricsCard: {
    marginBottom: 16,
    backgroundColor: theme.colors.surfaceVariant,
  },
  metricsTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 12,
  },
  metricsGrid: {
    gap: 8,
  },
  metricItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  metricLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 100,
  },
  metricBar: {
    flex: 1,
    height: 6,
    borderRadius: 3,
  },
  metricValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
    width: 40,
    textAlign: 'right',
  },
  tabContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  tabButton: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  emptyCard: {
    marginTop: 32,
  },
  emptyContent: {
    alignItems: 'center',
    padding: 32,
  },
  emptyTitle: {
    marginTop: 16,
    marginBottom: 8,
  },
  emptyText: {
    textAlign: 'center',
    marginBottom: 24,
    opacity: 0.7,
  },
  createButton: {
    backgroundColor: theme.colors.primary,
  },
  nodeCard: {
    marginBottom: 16,
    elevation: 2,
  },
  nodeHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  nodeInfo: {
    flex: 1,
    marginRight: 12,
  },
  nodeTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  nodeName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginLeft: 8,
    marginRight: 8,
  },
  layerBadge: {
    height: 20,
  },
  nodeMetaRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  typeChip: {
    height: 24,
  },
  activationText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  quantumStateContainer: {
    marginBottom: 16,
  },
  quantumStateTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  quantumMetrics: {
    gap: 6,
  },
  quantumMetricItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  quantumMetricLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 80,
  },
  quantumMetricBar: {
    flex: 1,
    height: 4,
    borderRadius: 2,
  },
  quantumMetricValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
    width: 50,
    textAlign: 'right',
  },
  divider: {
    marginVertical: 12,
  },
  parametersContainer: {
    marginBottom: 12,
  },
  parametersTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  parametersList: {
    gap: 4,
  },
  parameterItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  parameterLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  parameterValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
    flex: 1,
    textAlign: 'right',
  },
  lastUpdate: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  circuitCard: {
    marginBottom: 12,
    elevation: 2,
  },
  circuitHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  circuitInfo: {
    flex: 1,
    marginRight: 12,
  },
  circuitName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  circuitDescription: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 16,
  },
  statusChip: {
    height: 24,
  },
  circuitSpecs: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 12,
  },
  specItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  specText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    marginLeft: 4,
  },
  circuitMetrics: {
    marginBottom: 12,
  },
  resultsContainer: {
    marginBottom: 12,
  },
  resultsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  resultsList: {
    gap: 4,
  },
  resultItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  resultLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  resultValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
    flex: 1,
    textAlign: 'right',
  },
  executionTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  trainingCard: {
    marginBottom: 12,
    elevation: 2,
  },
  trainingHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  trainingInfo: {
    flex: 1,
    marginRight: 12,
  },
  trainingName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  trainingMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  modelChip: {
    height: 24,
    backgroundColor: theme.colors.primaryContainer,
  },
  datasetText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  progressContainer: {
    marginBottom: 12,
  },
  progressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  progressText: {
    fontSize: 14,
    color: theme.colors.onSurface,
  },
  progressPercentage: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.primary,
  },
  progressBar: {
    height: 6,
    borderRadius: 3,
  },
  metricsContainer: {
    marginBottom: 12,
  },
  metricsList: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  hyperparametersContainer: {
    marginBottom: 12,
  },
  hyperparametersTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  hyperparametersList: {
    gap: 4,
  },
  hyperparameterItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  hyperparameterLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  hyperparameterValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
  },
  hardwareContainer: {
    marginBottom: 12,
  },
  hardwareTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  hardwareSpecs: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  hardwareItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  hardwareText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    marginLeft: 4,
  },
  startTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.primary,
  },
});

export default GhostNeuroQScreen;