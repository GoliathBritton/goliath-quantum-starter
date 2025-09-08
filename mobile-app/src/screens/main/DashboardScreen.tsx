import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  RefreshControl,
  Dimensions,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  ProgressBar,
  Surface,
  Text,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { LineChart, PieChart } from 'react-native-chart-kit';

import { RootState, AppDispatch } from '../../store';
import { fetchBusinessPods, fetchOperations } from '../../store/slices/businessPodsSlice';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage';

const { width: screenWidth } = Dimensions.get('window');

const DashboardScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const { pods, operations, isLoading, error } = useSelector((state: RootState) => state.businessPods);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      await Promise.all([
        dispatch(fetchBusinessPods()),
        dispatch(fetchOperations()),
      ]);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
  };

  const getQuantumAdvantageData = () => {
    const labels = pods.map(pod => pod.name.split(' ')[0]);
    const data = pods.map(pod => pod.quantumAdvantage);
    
    return {
      labels,
      datasets: [
        {
          data,
          color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
          strokeWidth: 2,
        },
      ],
    };
  };

  const getPodStatusData = () => {
    const statusCounts = pods.reduce((acc, pod) => {
      acc[pod.status] = (acc[pod.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return [
      {
        name: 'Active',
        population: statusCounts.ACTIVE || 0,
        color: theme.colors.primary,
        legendFontColor: theme.colors.onSurface,
        legendFontSize: 12,
      },
      {
        name: 'Inactive',
        population: statusCounts.INACTIVE || 0,
        color: theme.colors.error,
        legendFontColor: theme.colors.onSurface,
        legendFontSize: 12,
      },
      {
        name: 'Maintenance',
        population: statusCounts.MAINTENANCE || 0,
        color: theme.colors.tertiary,
        legendFontColor: theme.colors.onSurface,
        legendFontSize: 12,
      },
    ];
  };

  const getRecentOperations = () => {
    return operations
      .sort((a, b) => new Date(b.startTime).getTime() - new Date(a.startTime).getTime())
      .slice(0, 5);
  };

  const getTotalQuantumAdvantage = () => {
    return pods.reduce((total, pod) => total + pod.quantumAdvantage, 0) / pods.length;
  };

  const getActiveOperationsCount = () => {
    return operations.filter(op => op.status === 'RUNNING' || op.status === 'PENDING').length;
  };

  if (isLoading && pods.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {error && <ErrorMessage message={error} />}
      
      {/* Welcome Section */}
      <Card style={styles.welcomeCard}>
        <Card.Content>
          <Title>Welcome back, {user?.name}!</Title>
          <Paragraph>Your quantum-enhanced business intelligence platform</Paragraph>
          <View style={styles.statsRow}>
            <View style={styles.statItem}>
              <Icon name="cube" size={24} color={theme.colors.primary} />
              <Text style={styles.statValue}>{pods.length}</Text>
              <Text style={styles.statLabel}>Business Pods</Text>
            </View>
            <View style={styles.statItem}>
              <Icon name="atom" size={24} color={theme.colors.secondary} />
              <Text style={styles.statValue}>{getTotalQuantumAdvantage().toFixed(1)}x</Text>
              <Text style={styles.statLabel}>Quantum Advantage</Text>
            </View>
            <View style={styles.statItem}>
              <Icon name="lightning-bolt" size={24} color={theme.colors.tertiary} />
              <Text style={styles.statValue}>{getActiveOperationsCount()}</Text>
              <Text style={styles.statLabel}>Active Operations</Text>
            </View>
          </View>
        </Card.Content>
      </Card>

      {/* Quantum Credits */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <Title>Quantum Credits</Title>
            <Chip icon="lightning-bolt" mode="outlined">
              {user?.quantumCredits || 0} credits
            </Chip>
          </View>
          <ProgressBar 
            progress={(user?.quantumCredits || 0) / 1000} 
            color={theme.colors.primary}
            style={styles.progressBar}
          />
          <Paragraph>Tier: {user?.tier}</Paragraph>
        </Card.Content>
      </Card>

      {/* Quantum Advantage Chart */}
      {pods.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Title>Quantum Advantage by Pod</Title>
            <LineChart
              data={getQuantumAdvantageData()}
              width={screenWidth - 60}
              height={220}
              chartConfig={{
                backgroundColor: theme.colors.surface,
                backgroundGradientFrom: theme.colors.surface,
                backgroundGradientTo: theme.colors.surface,
                decimalPlaces: 1,
                color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '6',
                  strokeWidth: '2',
                  stroke: theme.colors.primary,
                },
              }}
              bezier
              style={styles.chart}
            />
          </Card.Content>
        </Card>
      )}

      {/* Pod Status Distribution */}
      {pods.length > 0 && (
        <Card style={styles.card}>
          <Card.Content>
            <Title>Pod Status Distribution</Title>
            <PieChart
              data={getPodStatusData()}
              width={screenWidth - 60}
              height={220}
              chartConfig={{
                color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
              }}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              style={styles.chart}
            />
          </Card.Content>
        </Card>
      )}

      {/* Recent Operations */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Recent Operations</Title>
          {getRecentOperations().map((operation) => (
            <Surface key={operation.id} style={styles.operationItem}>
              <View style={styles.operationHeader}>
                <Text style={styles.operationType}>{operation.type}</Text>
                <Chip 
                  mode="outlined" 
                  textStyle={{
                    color: operation.status === 'COMPLETED' ? theme.colors.primary : 
                           operation.status === 'FAILED' ? theme.colors.error : 
                           theme.colors.tertiary
                  }}
                >
                  {operation.status}
                </Chip>
              </View>
              {operation.status === 'RUNNING' && (
                <ProgressBar 
                  progress={operation.progress / 100} 
                  color={theme.colors.primary}
                  style={styles.operationProgress}
                />
              )}
              <Text style={styles.operationTime}>
                {new Date(operation.startTime).toLocaleString()}
              </Text>
              {operation.quantumAdvantage && (
                <Text style={styles.quantumAdvantage}>
                  Quantum Advantage: {operation.quantumAdvantage.toFixed(2)}x
                </Text>
              )}
            </Surface>
          ))}
          {getRecentOperations().length === 0 && (
            <Paragraph>No recent operations</Paragraph>
          )}
        </Card.Content>
      </Card>

      {/* Quick Actions */}
      <Card style={styles.card}>
        <Card.Content>
          <Title>Quick Actions</Title>
          <View style={styles.actionButtons}>
            <Button 
              mode="contained" 
              icon="cube-outline"
              style={styles.actionButton}
              onPress={() => {/* Navigate to Business Pods */}}
            >
              View Pods
            </Button>
            <Button 
              mode="outlined" 
              icon="atom"
              style={styles.actionButton}
              onPress={() => {/* Navigate to Operations */}}
            >
              New Operation
            </Button>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  welcomeCard: {
    margin: 16,
    marginBottom: 8,
  },
  card: {
    margin: 16,
    marginTop: 8,
    marginBottom: 8,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    marginTop: 4,
  },
  statLabel: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
    marginTop: 2,
  },
  progressBar: {
    marginVertical: 8,
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  operationItem: {
    padding: 12,
    marginVertical: 4,
    borderRadius: 8,
  },
  operationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  operationType: {
    fontWeight: 'bold',
    fontSize: 16,
  },
  operationProgress: {
    marginVertical: 4,
  },
  operationTime: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
  },
  quantumAdvantage: {
    fontSize: 12,
    color: theme.colors.primary,
    fontWeight: 'bold',
    marginTop: 4,
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 8,
  },
});

export default DashboardScreen;