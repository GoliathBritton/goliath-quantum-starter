import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  RefreshControl,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Chip,
  FAB,
  Surface,
  Text,
  IconButton,
  Menu,
  Divider,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { 
  fetchBusinessPods, 
  scoreLeads, 
  optimizeEnergy, 
  optimizePortfolio,
  generateFinancialPlan,
  gatherIntelligence 
} from '../../store/slices/businessPodsSlice';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage';

interface PodAction {
  id: string;
  label: string;
  icon: string;
  action: (podId: string) => void;
}

const BusinessPodsScreen: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { pods, isLoading, error } = useSelector((state: RootState) => state.businessPods);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedPod, setSelectedPod] = useState<string | null>(null);
  const [menuVisible, setMenuVisible] = useState<string | null>(null);

  useEffect(() => {
    loadBusinessPods();
  }, []);

  const loadBusinessPods = async () => {
    try {
      await dispatch(fetchBusinessPods());
    } catch (error) {
      console.error('Failed to load business pods:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadBusinessPods();
    setRefreshing(false);
  };

  const handlePodAction = async (action: string, podId: string) => {
    try {
      setMenuVisible(null);
      
      switch (action) {
        case 'scoreLeads':
          await dispatch(scoreLeads({ podId, leads: [] }));
          Alert.alert('Success', 'Lead scoring initiated with quantum enhancement');
          break;
        case 'optimizeEnergy':
          await dispatch(optimizeEnergy({ podId, energyData: {} }));
          Alert.alert('Success', 'Energy optimization started');
          break;
        case 'optimizePortfolio':
          await dispatch(optimizePortfolio({ podId, portfolioData: {} }));
          Alert.alert('Success', 'Portfolio optimization in progress');
          break;
        case 'generatePlan':
          await dispatch(generateFinancialPlan({ podId, requirements: {} }));
          Alert.alert('Success', 'Financial plan generation started');
          break;
        case 'gatherIntel':
          await dispatch(gatherIntelligence({ podId, targets: [] }));
          Alert.alert('Success', 'Intelligence gathering initiated');
          break;
        default:
          Alert.alert('Info', `Action ${action} not implemented yet`);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to execute action');
    }
  };

  const getPodActions = (podType: string): PodAction[] => {
    const commonActions: PodAction[] = [
      {
        id: 'gatherIntel',
        label: 'Gather Intelligence',
        icon: 'brain',
        action: (podId) => handlePodAction('gatherIntel', podId),
      },
    ];

    switch (podType) {
      case 'SALES':
        return [
          {
            id: 'scoreLeads',
            label: 'Score Leads',
            icon: 'target',
            action: (podId) => handlePodAction('scoreLeads', podId),
          },
          ...commonActions,
        ];
      case 'ENERGY':
        return [
          {
            id: 'optimizeEnergy',
            label: 'Optimize Energy',
            icon: 'lightning-bolt',
            action: (podId) => handlePodAction('optimizeEnergy', podId),
          },
          ...commonActions,
        ];
      case 'FINANCE':
        return [
          {
            id: 'optimizePortfolio',
            label: 'Optimize Portfolio',
            icon: 'chart-line',
            action: (podId) => handlePodAction('optimizePortfolio', podId),
          },
          {
            id: 'generatePlan',
            label: 'Generate Plan',
            icon: 'file-document',
            action: (podId) => handlePodAction('generatePlan', podId),
          },
          ...commonActions,
        ];
      default:
        return commonActions;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return theme.colors.primary;
      case 'INACTIVE':
        return theme.colors.error;
      case 'MAINTENANCE':
        return theme.colors.tertiary;
      default:
        return theme.colors.onSurfaceVariant;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'SALES':
        return 'account-group';
      case 'ENERGY':
        return 'lightning-bolt';
      case 'FINANCE':
        return 'bank';
      case 'MARKETING':
        return 'bullhorn';
      case 'OPERATIONS':
        return 'cog';
      default:
        return 'cube';
    }
  };

  if (isLoading && pods.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <View style={styles.container}>
      <ScrollView
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {error && <ErrorMessage message={error} />}
        
        {/* Header Stats */}
        <Card style={styles.headerCard}>
          <Card.Content>
            <View style={styles.statsRow}>
              <View style={styles.statItem}>
                <Icon name="cube" size={32} color={theme.colors.primary} />
                <Text style={styles.statValue}>{pods.length}</Text>
                <Text style={styles.statLabel}>Total Pods</Text>
              </View>
              <View style={styles.statItem}>
                <Icon name="check-circle" size={32} color={theme.colors.primary} />
                <Text style={styles.statValue}>
                  {pods.filter(p => p.status === 'ACTIVE').length}
                </Text>
                <Text style={styles.statLabel}>Active</Text>
              </View>
              <View style={styles.statItem}>
                <Icon name="atom" size={32} color={theme.colors.secondary} />
                <Text style={styles.statValue}>
                  {pods.length > 0 ? 
                    (pods.reduce((sum, p) => sum + p.quantumAdvantage, 0) / pods.length).toFixed(1) : 
                    '0'
                  }x
                </Text>
                <Text style={styles.statLabel}>Avg Quantum</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Business Pods List */}
        {pods.map((pod) => (
          <Card key={pod.id} style={styles.podCard}>
            <Card.Content>
              <View style={styles.podHeader}>
                <View style={styles.podTitleRow}>
                  <Icon 
                    name={getTypeIcon(pod.type)} 
                    size={24} 
                    color={theme.colors.primary} 
                  />
                  <Title style={styles.podTitle}>{pod.name}</Title>
                </View>
                <Menu
                  visible={menuVisible === pod.id}
                  onDismiss={() => setMenuVisible(null)}
                  anchor={
                    <IconButton
                      icon="dots-vertical"
                      onPress={() => setMenuVisible(pod.id)}
                    />
                  }
                >
                  {getPodActions(pod.type).map((action) => (
                    <Menu.Item
                      key={action.id}
                      onPress={() => action.action(pod.id)}
                      title={action.label}
                      leadingIcon={action.icon}
                    />
                  ))}
                  <Divider />
                  <Menu.Item
                    onPress={() => {
                      setMenuVisible(null);
                      Alert.alert('Info', 'Pod settings not implemented yet');
                    }}
                    title="Settings"
                    leadingIcon="cog"
                  />
                </Menu>
              </View>
              
              <View style={styles.podDetails}>
                <Chip 
                  mode="outlined" 
                  textStyle={{ color: getStatusColor(pod.status) }}
                  style={{ borderColor: getStatusColor(pod.status) }}
                >
                  {pod.status}
                </Chip>
                <Chip mode="outlined">{pod.type}</Chip>
              </View>
              
              <Paragraph style={styles.podDescription}>
                {pod.description}
              </Paragraph>
              
              {/* Quantum Metrics */}
              <Surface style={styles.metricsContainer}>
                <View style={styles.metricItem}>
                  <Icon name="atom" size={20} color={theme.colors.secondary} />
                  <Text style={styles.metricLabel}>Quantum Advantage</Text>
                  <Text style={styles.metricValue}>{pod.quantumAdvantage.toFixed(2)}x</Text>
                </View>
                <View style={styles.metricItem}>
                  <Icon name="speedometer" size={20} color={theme.colors.tertiary} />
                  <Text style={styles.metricLabel}>Performance</Text>
                  <Text style={styles.metricValue}>{pod.performance.toFixed(1)}%</Text>
                </View>
                <View style={styles.metricItem}>
                  <Icon name="lightning-bolt" size={20} color={theme.colors.primary} />
                  <Text style={styles.metricLabel}>Efficiency</Text>
                  <Text style={styles.metricValue}>{pod.efficiency.toFixed(1)}%</Text>
                </View>
              </Surface>
              
              {/* Quick Actions */}
              <View style={styles.quickActions}>
                {getPodActions(pod.type).slice(0, 2).map((action) => (
                  <Button
                    key={action.id}
                    mode="outlined"
                    icon={action.icon}
                    style={styles.quickActionButton}
                    onPress={() => action.action(pod.id)}
                    compact
                  >
                    {action.label}
                  </Button>
                ))}
              </View>
            </Card.Content>
          </Card>
        ))}
        
        {pods.length === 0 && !isLoading && (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Icon name="cube-outline" size={64} color={theme.colors.onSurfaceVariant} />
              <Title style={styles.emptyTitle}>No Business Pods</Title>
              <Paragraph style={styles.emptyText}>
                Create your first quantum-enhanced business pod to get started
              </Paragraph>
              <Button 
                mode="contained" 
                icon="plus"
                style={styles.createButton}
                onPress={() => Alert.alert('Info', 'Pod creation not implemented yet')}
              >
                Create Pod
              </Button>
            </Card.Content>
          </Card>
        )}
      </ScrollView>
      
      {/* Floating Action Button */}
      <FAB
        style={styles.fab}
        icon="plus"
        onPress={() => Alert.alert('Info', 'Pod creation not implemented yet')}
        label="New Pod"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  headerCard: {
    margin: 16,
    marginBottom: 8,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
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
  podCard: {
    margin: 16,
    marginTop: 8,
    marginBottom: 8,
  },
  podHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  podTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  podTitle: {
    marginLeft: 8,
    flex: 1,
  },
  podDetails: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  podDescription: {
    marginBottom: 16,
    color: theme.colors.onSurfaceVariant,
  },
  metricsContainer: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  metricItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  metricLabel: {
    marginLeft: 8,
    flex: 1,
    fontSize: 14,
  },
  metricValue: {
    fontWeight: 'bold',
    fontSize: 14,
  },
  quickActions: {
    flexDirection: 'row',
    gap: 8,
  },
  quickActionButton: {
    flex: 1,
  },
  emptyCard: {
    margin: 16,
    marginTop: 32,
  },
  emptyContent: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  emptyTitle: {
    marginTop: 16,
    marginBottom: 8,
  },
  emptyText: {
    textAlign: 'center',
    marginBottom: 24,
    color: theme.colors.onSurfaceVariant,
  },
  createButton: {
    marginTop: 8,
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
  },
});

export default BusinessPodsScreen;