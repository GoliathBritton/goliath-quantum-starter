import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert,
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
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface QuantumOperationsScreenProps {
  navigation: any;
}

interface QuantumOperation {
  id: string;
  name: string;
  type: 'circuit' | 'algorithm' | 'simulation' | 'optimization';
  status: 'running' | 'completed' | 'failed' | 'queued';
  progress: number;
  qubits: number;
  gates: number;
  duration: number;
  createdAt: string;
  description: string;
}

const QuantumOperationsScreen: React.FC<QuantumOperationsScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [operations, setOperations] = useState<QuantumOperation[]>([]);
  const [filter, setFilter] = useState<'all' | 'running' | 'completed' | 'failed'>('all');

  useEffect(() => {
    loadOperations();
  }, []);

  const loadOperations = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data
      const mockOperations: QuantumOperation[] = [
        {
          id: '1',
          name: 'Quantum Fourier Transform',
          type: 'circuit',
          status: 'running',
          progress: 0.65,
          qubits: 8,
          gates: 24,
          duration: 1200,
          createdAt: new Date().toISOString(),
          description: 'Implementing QFT for quantum phase estimation'
        },
        {
          id: '2',
          name: 'Grover Search Algorithm',
          type: 'algorithm',
          status: 'completed',
          progress: 1.0,
          qubits: 4,
          gates: 16,
          duration: 850,
          createdAt: new Date(Date.now() - 3600000).toISOString(),
          description: 'Searching unsorted database with quantum speedup'
        },
        {
          id: '3',
          name: 'VQE Optimization',
          type: 'optimization',
          status: 'failed',
          progress: 0.3,
          qubits: 6,
          gates: 32,
          duration: 0,
          createdAt: new Date(Date.now() - 7200000).toISOString(),
          description: 'Variational Quantum Eigensolver for molecular simulation'
        },
        {
          id: '4',
          name: 'Quantum Simulation',
          type: 'simulation',
          status: 'queued',
          progress: 0,
          qubits: 12,
          gates: 48,
          duration: 0,
          createdAt: new Date(Date.now() - 1800000).toISOString(),
          description: 'Simulating quantum many-body system dynamics'
        }
      ];
      
      setOperations(mockOperations);
    } catch (error) {
      console.error('Load operations error:', error);
      Alert.alert('Error', 'Failed to load quantum operations');
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadOperations();
    setRefreshing(false);
  };

  const getStatusColor = (status: QuantumOperation['status']) => {
    switch (status) {
      case 'running':
        return theme.colors.primary;
      case 'completed':
        return theme.colors.tertiary;
      case 'failed':
        return theme.colors.error;
      case 'queued':
        return theme.colors.outline;
      default:
        return theme.colors.outline;
    }
  };

  const getTypeIcon = (type: QuantumOperation['type']) => {
    switch (type) {
      case 'circuit':
        return 'resistor-nodes';
      case 'algorithm':
        return 'function-variant';
      case 'simulation':
        return 'atom';
      case 'optimization':
        return 'chart-line';
      default:
        return 'cog';
    }
  };

  const filteredOperations = operations.filter(op => 
    filter === 'all' || op.status === filter
  );

  const handleOperationPress = (operation: QuantumOperation) => {
    navigation.navigate('QuantumOperationDetails', { operationId: operation.id });
  };

  const handleCreateOperation = () => {
    navigation.navigate('CreateQuantumOperation');
  };

  const formatDuration = (seconds: number) => {
    if (seconds === 0) return 'N/A';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  if (isLoading && operations.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading quantum operations..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>Quantum Operations</Title>
        <Paragraph style={styles.subtitle}>
          Monitor and manage your quantum computations
        </Paragraph>
        
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          style={styles.filterContainer}
        >
          {(['all', 'running', 'completed', 'failed'] as const).map((filterType) => (
            <Chip
              key={filterType}
              selected={filter === filterType}
              onPress={() => setFilter(filterType)}
              style={styles.filterChip}
              textStyle={{
                color: filter === filterType ? theme.colors.onPrimary : theme.colors.onSurface
              }}
            >
              {filterType.charAt(0).toUpperCase() + filterType.slice(1)}
            </Chip>
          ))}
        </ScrollView>
      </Surface>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {filteredOperations.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Icon name="atom" size={64} color={theme.colors.outline} />
              <Title style={styles.emptyTitle}>No Operations Found</Title>
              <Paragraph style={styles.emptyText}>
                {filter === 'all' 
                  ? 'Start your first quantum operation to see it here'
                  : `No ${filter} operations found`
                }
              </Paragraph>
              <Button 
                mode="contained" 
                onPress={handleCreateOperation}
                style={styles.createButton}
              >
                Create Operation
              </Button>
            </Card.Content>
          </Card>
        ) : (
          filteredOperations.map((operation) => (
            <Card 
              key={operation.id} 
              style={styles.operationCard}
              onPress={() => handleOperationPress(operation)}
            >
              <Card.Content>
                <View style={styles.operationHeader}>
                  <View style={styles.operationInfo}>
                    <View style={styles.operationTitleRow}>
                      <Icon 
                        name={getTypeIcon(operation.type)} 
                        size={20} 
                        color={theme.colors.primary} 
                      />
                      <Text style={styles.operationName}>{operation.name}</Text>
                    </View>
                    <Text style={styles.operationDescription}>
                      {operation.description}
                    </Text>
                  </View>
                  <Chip 
                    style={[styles.statusChip, { backgroundColor: getStatusColor(operation.status) }]}
                    textStyle={{ color: theme.colors.onPrimary }}
                  >
                    {operation.status}
                  </Chip>
                </View>

                {operation.status === 'running' && (
                  <View style={styles.progressContainer}>
                    <View style={styles.progressHeader}>
                      <Text style={styles.progressText}>Progress</Text>
                      <Text style={styles.progressPercentage}>
                        {Math.round(operation.progress * 100)}%
                      </Text>
                    </View>
                    <ProgressBar 
                      progress={operation.progress} 
                      color={theme.colors.primary}
                      style={styles.progressBar}
                    />
                  </View>
                )}

                <Divider style={styles.divider} />

                <View style={styles.operationStats}>
                  <View style={styles.statItem}>
                    <Icon name="memory" size={16} color={theme.colors.outline} />
                    <Text style={styles.statText}>{operation.qubits} qubits</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Icon name="gate-and" size={16} color={theme.colors.outline} />
                    <Text style={styles.statText}>{operation.gates} gates</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Icon name="clock-outline" size={16} color={theme.colors.outline} />
                    <Text style={styles.statText}>{formatDuration(operation.duration)}</Text>
                  </View>
                </View>
              </Card.Content>
            </Card>
          ))
        )}
      </ScrollView>

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={handleCreateOperation}
        label="New Operation"
      />
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
  filterContainer: {
    flexDirection: 'row',
  },
  filterChip: {
    marginRight: 8,
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
  operationCard: {
    marginBottom: 12,
    elevation: 2,
  },
  operationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  operationInfo: {
    flex: 1,
    marginRight: 12,
  },
  operationTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  operationName: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginLeft: 8,
  },
  operationDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 20,
  },
  statusChip: {
    height: 28,
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
  divider: {
    marginVertical: 12,
  },
  operationStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    marginLeft: 4,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.primary,
  },
});

export default QuantumOperationsScreen;