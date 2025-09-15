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
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
// import { LineChart, BarChart } from 'react-native-chart-kit'; // Removed for compatibility

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface SFGSymmetryScreenProps {
  navigation: any;
}

interface SymmetryPattern {
  id: string;
  name: string;
  type: 'geometric' | 'algebraic' | 'topological' | 'quantum';
  complexity: number;
  stability: number;
  efficiency: number;
  description: string;
  applications: string[];
  status: 'active' | 'inactive' | 'experimental';
  createdAt: string;
  lastModified: string;
  parameters: {
    dimensions: number;
    symmetryGroup: string;
    invariants: string[];
    transformations: number;
  };
}

interface SymmetryAnalysis {
  id: string;
  patternId: string;
  title: string;
  type: 'structure' | 'dynamics' | 'optimization' | 'prediction';
  status: 'running' | 'completed' | 'failed' | 'queued';
  progress: number;
  results?: {
    symmetryScore: number;
    breakingPoints: number[];
    conservedQuantities: string[];
    emergentProperties: string[];
  };
  startTime: string;
  estimatedCompletion?: string;
  computeResources: {
    cpuUsage: number;
    memoryUsage: number;
    quantumQubits: number;
  };
}

interface FieldConfiguration {
  id: string;
  name: string;
  fieldType: 'scalar' | 'vector' | 'tensor' | 'spinor';
  dimensions: number;
  boundary: 'periodic' | 'open' | 'fixed' | 'absorbing';
  symmetries: string[];
  energy: number;
  stability: number;
  isActive: boolean;
  parameters: Record<string, number>;
}

const SFGSymmetryScreen: React.FC<SFGSymmetryScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [patterns, setPatterns] = useState<SymmetryPattern[]>([]);
  const [analyses, setAnalyses] = useState<SymmetryAnalysis[]>([]);
  const [fieldConfigs, setFieldConfigs] = useState<FieldConfiguration[]>([]);
  const [activeTab, setActiveTab] = useState<'patterns' | 'analyses' | 'fields'>('patterns');
  const [systemStatus, setSystemStatus] = useState({
    quantumCoherence: 0.94,
    fieldStability: 0.87,
    symmetryPreservation: 0.91,
    computationalLoad: 0.68
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock patterns data
      const mockPatterns: SymmetryPattern[] = [
        {
          id: '1',
          name: 'SU(3) Color Symmetry',
          type: 'algebraic',
          complexity: 0.85,
          stability: 0.92,
          efficiency: 0.88,
          description: 'Strong force color symmetry in quantum chromodynamics',
          applications: ['Particle Physics', 'Quantum Field Theory', 'Gauge Theory'],
          status: 'active',
          createdAt: new Date(Date.now() - 86400000).toISOString(),
          lastModified: new Date(Date.now() - 3600000).toISOString(),
          parameters: {
            dimensions: 8,
            symmetryGroup: 'SU(3)',
            invariants: ['Color Charge', 'Baryon Number'],
            transformations: 24
          }
        },
        {
          id: '2',
          name: 'Crystalline Lattice',
          type: 'geometric',
          complexity: 0.65,
          stability: 0.96,
          efficiency: 0.91,
          description: 'Periodic geometric symmetry in crystal structures',
          applications: ['Materials Science', 'Solid State Physics', 'Nanotechnology'],
          status: 'active',
          createdAt: new Date(Date.now() - 172800000).toISOString(),
          lastModified: new Date(Date.now() - 7200000).toISOString(),
          parameters: {
            dimensions: 3,
            symmetryGroup: 'P6/mmm',
            invariants: ['Lattice Constant', 'Unit Cell'],
            transformations: 12
          }
        },
        {
          id: '3',
          name: 'Quantum Entanglement Network',
          type: 'quantum',
          complexity: 0.94,
          stability: 0.78,
          efficiency: 0.82,
          description: 'Non-local quantum correlations preserving entanglement symmetry',
          applications: ['Quantum Computing', 'Quantum Communication', 'Cryptography'],
          status: 'experimental',
          createdAt: new Date(Date.now() - 259200000).toISOString(),
          lastModified: new Date(Date.now() - 1800000).toISOString(),
          parameters: {
            dimensions: 16,
            symmetryGroup: 'Bell States',
            invariants: ['Entanglement Entropy', 'Concurrence'],
            transformations: 64
          }
        },
        {
          id: '4',
          name: 'Topological Invariant',
          type: 'topological',
          complexity: 0.89,
          stability: 0.85,
          efficiency: 0.79,
          description: 'Topologically protected quantum states with robust symmetries',
          applications: ['Quantum Error Correction', 'Topological Computing', 'Anyons'],
          status: 'active',
          createdAt: new Date(Date.now() - 345600000).toISOString(),
          lastModified: new Date(Date.now() - 10800000).toISOString(),
          parameters: {
            dimensions: 2,
            symmetryGroup: 'Z2',
            invariants: ['Chern Number', 'Winding Number'],
            transformations: 4
          }
        }
      ];
      
      // Mock analyses data
      const mockAnalyses: SymmetryAnalysis[] = [
        {
          id: '1',
          patternId: '1',
          title: 'Color Confinement Analysis',
          type: 'dynamics',
          status: 'running',
          progress: 0.73,
          startTime: new Date(Date.now() - 1800000).toISOString(),
          estimatedCompletion: new Date(Date.now() + 900000).toISOString(),
          computeResources: {
            cpuUsage: 0.85,
            memoryUsage: 0.67,
            quantumQubits: 32
          }
        },
        {
          id: '2',
          patternId: '2',
          title: 'Lattice Defect Impact',
          type: 'structure',
          status: 'completed',
          progress: 1.0,
          results: {
            symmetryScore: 0.94,
            breakingPoints: [0.15, 0.32, 0.78],
            conservedQuantities: ['Energy', 'Momentum', 'Angular Momentum'],
            emergentProperties: ['Phonon Modes', 'Elastic Constants']
          },
          startTime: new Date(Date.now() - 7200000).toISOString(),
          computeResources: {
            cpuUsage: 0.45,
            memoryUsage: 0.32,
            quantumQubits: 16
          }
        },
        {
          id: '3',
          patternId: '3',
          title: 'Entanglement Preservation',
          type: 'optimization',
          status: 'queued',
          progress: 0,
          startTime: new Date().toISOString(),
          estimatedCompletion: new Date(Date.now() + 3600000).toISOString(),
          computeResources: {
            cpuUsage: 0,
            memoryUsage: 0,
            quantumQubits: 64
          }
        },
        {
          id: '4',
          patternId: '4',
          title: 'Topological Protection',
          type: 'prediction',
          status: 'failed',
          progress: 0.23,
          startTime: new Date(Date.now() - 3600000).toISOString(),
          computeResources: {
            cpuUsage: 0.12,
            memoryUsage: 0.08,
            quantumQubits: 8
          }
        }
      ];
      
      // Mock field configurations
      const mockFieldConfigs: FieldConfiguration[] = [
        {
          id: '1',
          name: 'Electromagnetic Field',
          fieldType: 'vector',
          dimensions: 4,
          boundary: 'open',
          symmetries: ['U(1)', 'Lorentz'],
          energy: 1247.5,
          stability: 0.96,
          isActive: true,
          parameters: {
            coupling: 0.137,
            frequency: 2.45e9,
            amplitude: 1.0,
            phase: 0.0
          }
        },
        {
          id: '2',
          name: 'Higgs Field',
          fieldType: 'scalar',
          dimensions: 4,
          boundary: 'periodic',
          symmetries: ['SU(2)', 'U(1)'],
          energy: 246.2,
          stability: 0.89,
          isActive: true,
          parameters: {
            vev: 246.2,
            mass: 125.1,
            lambda: 0.13,
            beta: 0.0
          }
        },
        {
          id: '3',
          name: 'Gravitational Field',
          fieldType: 'tensor',
          dimensions: 4,
          boundary: 'fixed',
          symmetries: ['Diffeomorphism', 'Local Lorentz'],
          energy: 0.0,
          stability: 0.99,
          isActive: false,
          parameters: {
            newton_g: 6.67e-11,
            cosmological: 1.19e-52,
            curvature: 0.0,
            torsion: 0.0
          }
        },
        {
          id: '4',
          name: 'Quantum Spinor Field',
          fieldType: 'spinor',
          dimensions: 4,
          boundary: 'absorbing',
          symmetries: ['SU(2)', 'Chiral'],
          energy: 938.3,
          stability: 0.87,
          isActive: true,
          parameters: {
            mass: 0.511,
            spin: 0.5,
            charge: -1.0,
            magnetic_moment: -1.001
          }
        }
      ];
      
      setPatterns(mockPatterns);
      setAnalyses(mockAnalyses);
      setFieldConfigs(mockFieldConfigs);
      
    } catch (error) {
      console.error('Load data error:', error);
      Alert.alert('Error', 'Failed to load SFG Symmetry data');
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
      case 'completed':
        return theme.colors.primary;
      case 'experimental':
      case 'queued':
        return theme.colors.tertiary;
      case 'inactive':
      case 'failed':
        return theme.colors.error;
      default:
        return theme.colors.outline;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'geometric':
        return '#4CAF50';
      case 'algebraic':
        return '#2196F3';
      case 'topological':
        return '#FF9800';
      case 'quantum':
        return '#9C27B0';
      case 'scalar':
        return '#607D8B';
      case 'vector':
        return '#795548';
      case 'tensor':
        return '#E91E63';
      case 'spinor':
        return '#00BCD4';
      default:
        return theme.colors.outline;
    }
  };

  const formatNumber = (value: number, decimals: number = 2) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const handlePatternPress = (pattern: SymmetryPattern) => {
    navigation.navigate('PatternDetails', { patternId: pattern.id });
  };

  const handleAnalysisPress = (analysis: SymmetryAnalysis) => {
    navigation.navigate('AnalysisDetails', { analysisId: analysis.id });
  };

  const handleFieldToggle = (fieldId: string) => {
    setFieldConfigs(prev => prev.map(field => 
      field.id === fieldId ? { ...field, isActive: !field.isActive } : field
    ));
  };

  const handleCreatePattern = () => {
    navigation.navigate('CreatePattern');
  };

  const handleCreateAnalysis = () => {
    navigation.navigate('CreateAnalysis');
  };

  if (isLoading && patterns.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading SFG Symmetry..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>SFG Symmetry</Title>
        <Paragraph style={styles.subtitle}>
          Symmetry Field Generator - Advanced symmetry analysis and field manipulation
        </Paragraph>
        
        {/* System Status */}
        <Card style={styles.statusCard}>
          <Card.Content>
            <Text style={styles.statusTitle}>System Status</Text>
            <View style={styles.statusGrid}>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Quantum Coherence</Text>
                <ProgressBar 
                  progress={systemStatus.quantumCoherence} 
                  color={theme.colors.primary}
                  style={styles.statusBar}
                />
                <Text style={styles.statusValue}>{formatPercentage(systemStatus.quantumCoherence)}</Text>
              </View>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Field Stability</Text>
                <ProgressBar 
                  progress={systemStatus.fieldStability} 
                  color={theme.colors.secondary}
                  style={styles.statusBar}
                />
                <Text style={styles.statusValue}>{formatPercentage(systemStatus.fieldStability)}</Text>
              </View>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Symmetry Preservation</Text>
                <ProgressBar 
                  progress={systemStatus.symmetryPreservation} 
                  color={theme.colors.tertiary}
                  style={styles.statusBar}
                />
                <Text style={styles.statusValue}>{formatPercentage(systemStatus.symmetryPreservation)}</Text>
              </View>
              <View style={styles.statusItem}>
                <Text style={styles.statusLabel}>Computational Load</Text>
                <ProgressBar 
                  progress={systemStatus.computationalLoad} 
                  color={theme.colors.error}
                  style={styles.statusBar}
                />
                <Text style={styles.statusValue}>{formatPercentage(systemStatus.computationalLoad)}</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
        
        <View style={styles.tabContainer}>
          <Button
            mode={activeTab === 'patterns' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('patterns')}
            style={styles.tabButton}
            compact
          >
            Patterns
          </Button>
          <Button
            mode={activeTab === 'analyses' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('analyses')}
            style={styles.tabButton}
            compact
          >
            Analyses
          </Button>
          <Button
            mode={activeTab === 'fields' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('fields')}
            style={styles.tabButton}
            compact
          >
            Fields
          </Button>
        </View>
      </Surface>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'patterns' ? (
          patterns.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="symmetry" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Symmetry Patterns</Title>
                <Paragraph style={styles.emptyText}>
                  Create your first symmetry pattern to get started
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreatePattern}
                  style={styles.createButton}
                >
                  Create Pattern
                </Button>
              </Card.Content>
            </Card>
          ) : (
            patterns.map((pattern) => (
              <Card 
                key={pattern.id} 
                style={styles.patternCard}
                onPress={() => handlePatternPress(pattern)}
              >
                <Card.Content>
                  <View style={styles.patternHeader}>
                    <View style={styles.patternInfo}>
                      <Text style={styles.patternName}>{pattern.name}</Text>
                      <Text style={styles.patternDescription}>{pattern.description}</Text>
                    </View>
                    <View style={styles.patternBadges}>
                      <Chip 
                        style={[styles.typeChip, { backgroundColor: getTypeColor(pattern.type) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {pattern.type}
                      </Chip>
                      <Chip 
                        style={[styles.statusChip, { backgroundColor: getStatusColor(pattern.status) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {pattern.status}
                      </Chip>
                    </View>
                  </View>

                  <View style={styles.metricsContainer}>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Complexity</Text>
                      <ProgressBar 
                        progress={pattern.complexity} 
                        color={theme.colors.primary}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(pattern.complexity)}</Text>
                    </View>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Stability</Text>
                      <ProgressBar 
                        progress={pattern.stability} 
                        color={theme.colors.secondary}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(pattern.stability)}</Text>
                    </View>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Efficiency</Text>
                      <ProgressBar 
                        progress={pattern.efficiency} 
                        color={theme.colors.tertiary}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(pattern.efficiency)}</Text>
                    </View>
                  </View>

                  <Divider style={styles.divider} />

                  <View style={styles.parametersContainer}>
                    <Text style={styles.parametersTitle}>Parameters</Text>
                    <View style={styles.parametersList}>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Dimensions:</Text>
                        <Text style={styles.parameterValue}>{pattern.parameters.dimensions}</Text>
                      </View>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Group:</Text>
                        <Text style={styles.parameterValue}>{pattern.parameters.symmetryGroup}</Text>
                      </View>
                      <View style={styles.parameterItem}>
                        <Text style={styles.parameterLabel}>Transformations:</Text>
                        <Text style={styles.parameterValue}>{pattern.parameters.transformations}</Text>
                      </View>
                    </View>
                  </View>

                  <View style={styles.applicationsContainer}>
                    <Text style={styles.applicationsTitle}>Applications:</Text>
                    <View style={styles.applicationsList}>
                      {pattern.applications.map((app, index) => (
                        <Chip key={index} style={styles.applicationChip} compact>
                          {app}
                        </Chip>
                      ))}
                    </View>
                  </View>

                  <Text style={styles.lastModified}>
                    Modified: {new Date(pattern.lastModified).toLocaleString()}
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        ) : activeTab === 'analyses' ? (
          analyses.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="chart-line" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Active Analyses</Title>
                <Paragraph style={styles.emptyText}>
                  Start a new symmetry analysis to get insights
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreateAnalysis}
                  style={styles.createButton}
                >
                  Start Analysis
                </Button>
              </Card.Content>
            </Card>
          ) : (
            analyses.map((analysis) => {
              const pattern = patterns.find(p => p.id === analysis.patternId);
              return (
                <Card 
                  key={analysis.id} 
                  style={styles.analysisCard}
                  onPress={() => handleAnalysisPress(analysis)}
                >
                  <Card.Content>
                    <View style={styles.analysisHeader}>
                      <View style={styles.analysisInfo}>
                        <Text style={styles.analysisTitle}>{analysis.title}</Text>
                        <Text style={styles.analysisPattern}>
                          Pattern: {pattern?.name || 'Unknown'}
                        </Text>
                      </View>
                      <Chip 
                        style={[styles.statusChip, { backgroundColor: getStatusColor(analysis.status) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {analysis.status}
                      </Chip>
                    </View>

                    {analysis.status === 'running' && (
                      <View style={styles.progressContainer}>
                        <View style={styles.progressHeader}>
                          <Text style={styles.progressText}>Progress</Text>
                          <Text style={styles.progressPercentage}>
                            {Math.round(analysis.progress * 100)}%
                          </Text>
                        </View>
                        <ProgressBar 
                          progress={analysis.progress} 
                          color={theme.colors.primary}
                          style={styles.progressBar}
                        />
                      </View>
                    )}

                    {analysis.results && (
                      <View style={styles.resultsContainer}>
                        <Text style={styles.resultsTitle}>Results</Text>
                        <View style={styles.resultItem}>
                          <Text style={styles.resultLabel}>Symmetry Score:</Text>
                          <Text style={styles.resultValue}>
                            {formatPercentage(analysis.results.symmetryScore)}
                          </Text>
                        </View>
                        <View style={styles.resultItem}>
                          <Text style={styles.resultLabel}>Breaking Points:</Text>
                          <Text style={styles.resultValue}>
                            {analysis.results.breakingPoints.length}
                          </Text>
                        </View>
                        <View style={styles.resultItem}>
                          <Text style={styles.resultLabel}>Conserved Quantities:</Text>
                          <Text style={styles.resultValue}>
                            {analysis.results.conservedQuantities.join(', ')}
                          </Text>
                        </View>
                      </View>
                    )}

                    <Divider style={styles.divider} />

                    <View style={styles.resourcesContainer}>
                      <Text style={styles.resourcesTitle}>Compute Resources</Text>
                      <View style={styles.resourcesList}>
                        <View style={styles.resourceItem}>
                          <Icon name="cpu-64-bit" size={16} color={theme.colors.primary} />
                          <Text style={styles.resourceText}>
                            CPU: {formatPercentage(analysis.computeResources.cpuUsage)}
                          </Text>
                        </View>
                        <View style={styles.resourceItem}>
                          <Icon name="memory" size={16} color={theme.colors.secondary} />
                          <Text style={styles.resourceText}>
                            Memory: {formatPercentage(analysis.computeResources.memoryUsage)}
                          </Text>
                        </View>
                        <View style={styles.resourceItem}>
                          <Icon name="atom" size={16} color={theme.colors.tertiary} />
                          <Text style={styles.resourceText}>
                            Qubits: {analysis.computeResources.quantumQubits}
                          </Text>
                        </View>
                      </View>
                    </View>

                    <Text style={styles.startTime}>
                      Started: {new Date(analysis.startTime).toLocaleString()}
                    </Text>
                  </Card.Content>
                </Card>
              );
            })
          )
        ) : (
          fieldConfigs.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="waves" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Field Configurations</Title>
                <Paragraph style={styles.emptyText}>
                  Configure your first quantum field to get started
                </Paragraph>
              </Card.Content>
            </Card>
          ) : (
            fieldConfigs.map((field) => (
              <Card key={field.id} style={styles.fieldCard}>
                <Card.Content>
                  <View style={styles.fieldHeader}>
                    <View style={styles.fieldInfo}>
                      <Text style={styles.fieldName}>{field.name}</Text>
                      <View style={styles.fieldMeta}>
                        <Chip 
                          style={[styles.typeChip, { backgroundColor: getTypeColor(field.fieldType) }]}
                          textStyle={{ color: theme.colors.onPrimary }}
                          compact
                        >
                          {field.fieldType}
                        </Chip>
                        <Chip 
                          style={styles.dimensionChip}
                          compact
                        >
                          {field.dimensions}D
                        </Chip>
                      </View>
                    </View>
                    <Switch
                      value={field.isActive}
                      onValueChange={() => handleFieldToggle(field.id)}
                      color={theme.colors.primary}
                    />
                  </View>

                  <View style={styles.fieldMetrics}>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Energy</Text>
                      <Text style={styles.metricValue}>{formatNumber(field.energy)} GeV</Text>
                    </View>
                    <View style={styles.metricItem}>
                      <Text style={styles.metricLabel}>Stability</Text>
                      <ProgressBar 
                        progress={field.stability} 
                        color={theme.colors.primary}
                        style={styles.metricBar}
                      />
                      <Text style={styles.metricValue}>{formatPercentage(field.stability)}</Text>
                    </View>
                  </View>

                  <View style={styles.symmetriesContainer}>
                    <Text style={styles.symmetriesTitle}>Symmetries:</Text>
                    <View style={styles.symmetriesList}>
                      {field.symmetries.map((symmetry, index) => (
                        <Chip key={index} style={styles.symmetryChip} compact>
                          {symmetry}
                        </Chip>
                      ))}
                    </View>
                  </View>

                  <View style={styles.boundaryContainer}>
                    <Text style={styles.boundaryLabel}>Boundary Conditions:</Text>
                    <Text style={styles.boundaryValue}>{field.boundary}</Text>
                  </View>
                </Card.Content>
              </Card>
            ))
          )
        )}
      </ScrollView>

      {(activeTab === 'patterns' || activeTab === 'analyses') && (
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={activeTab === 'patterns' ? handleCreatePattern : handleCreateAnalysis}
          label={activeTab === 'patterns' ? 'New Pattern' : 'New Analysis'}
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
  statusCard: {
    marginBottom: 16,
    backgroundColor: theme.colors.surfaceVariant,
  },
  statusTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 12,
  },
  statusGrid: {
    gap: 8,
  },
  statusItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  statusLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 120,
  },
  statusBar: {
    flex: 1,
    height: 6,
    borderRadius: 3,
  },
  statusValue: {
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
  patternCard: {
    marginBottom: 16,
    elevation: 2,
  },
  patternHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  patternInfo: {
    flex: 1,
    marginRight: 12,
  },
  patternName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  patternDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 20,
  },
  patternBadges: {
    gap: 4,
  },
  typeChip: {
    height: 24,
  },
  statusChip: {
    height: 24,
  },
  metricsContainer: {
    marginBottom: 16,
  },
  metricItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  metricLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 80,
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
  },
  applicationsContainer: {
    marginBottom: 12,
  },
  applicationsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  applicationsList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  applicationChip: {
    marginRight: 6,
    marginBottom: 4,
    backgroundColor: theme.colors.surfaceVariant,
  },
  lastModified: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  analysisCard: {
    marginBottom: 12,
    elevation: 2,
  },
  analysisHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  analysisInfo: {
    flex: 1,
    marginRight: 12,
  },
  analysisTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  analysisPattern: {
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
  resultsContainer: {
    marginBottom: 12,
  },
  resultsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  resultItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 4,
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
  resourcesContainer: {
    marginBottom: 12,
  },
  resourcesTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  resourcesList: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  resourceItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  resourceText: {
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
  fieldCard: {
    marginBottom: 12,
    elevation: 2,
  },
  fieldHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  fieldInfo: {
    flex: 1,
  },
  fieldName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  fieldMeta: {
    flexDirection: 'row',
    gap: 8,
  },
  dimensionChip: {
    height: 24,
    backgroundColor: theme.colors.surfaceVariant,
  },
  fieldMetrics: {
    marginBottom: 12,
  },
  symmetriesContainer: {
    marginBottom: 12,
  },
  symmetriesTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  symmetriesList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  symmetryChip: {
    marginRight: 6,
    marginBottom: 4,
    backgroundColor: theme.colors.primaryContainer,
  },
  boundaryContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  boundaryLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  boundaryValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.primary,
  },
});

export default SFGSymmetryScreen;