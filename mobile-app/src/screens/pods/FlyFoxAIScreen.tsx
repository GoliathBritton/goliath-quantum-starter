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
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface FlyFoxAIScreenProps {
  navigation: any;
}

interface AIAgent {
  id: string;
  name: string;
  type: 'assistant' | 'analyzer' | 'optimizer' | 'predictor' | 'generator';
  status: 'active' | 'idle' | 'training' | 'offline';
  capabilities: string[];
  performance: {
    accuracy: number;
    speed: number;
    efficiency: number;
  };
  usage: {
    totalTasks: number;
    successRate: number;
    avgResponseTime: number;
  };
  description: string;
  lastActive: string;
  version: string;
}

interface AITask {
  id: string;
  title: string;
  type: 'analysis' | 'optimization' | 'prediction' | 'generation';
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  assignedAgent: string;
  createdAt: string;
  estimatedCompletion: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

const FlyFoxAIScreen: React.FC<FlyFoxAIScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [agents, setAgents] = useState<AIAgent[]>([]);
  const [tasks, setTasks] = useState<AITask[]>([]);
  const [activeTab, setActiveTab] = useState<'agents' | 'tasks'>('agents');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock agents data
      const mockAgents: AIAgent[] = [
        {
          id: '1',
          name: 'Quantum Analyst',
          type: 'analyzer',
          status: 'active',
          capabilities: ['Data Analysis', 'Pattern Recognition', 'Quantum Computing'],
          performance: {
            accuracy: 0.94,
            speed: 0.87,
            efficiency: 0.91
          },
          usage: {
            totalTasks: 1247,
            successRate: 0.96,
            avgResponseTime: 2.3
          },
          description: 'Advanced AI agent specialized in quantum data analysis and pattern recognition',
          lastActive: new Date().toISOString(),
          version: '3.2.1'
        },
        {
          id: '2',
          name: 'Neural Optimizer',
          type: 'optimizer',
          status: 'active',
          capabilities: ['Hyperparameter Tuning', 'Model Optimization', 'Resource Management'],
          performance: {
            accuracy: 0.89,
            speed: 0.92,
            efficiency: 0.88
          },
          usage: {
            totalTasks: 856,
            successRate: 0.93,
            avgResponseTime: 4.1
          },
          description: 'Intelligent optimization agent for neural networks and quantum algorithms',
          lastActive: new Date(Date.now() - 300000).toISOString(),
          version: '2.8.4'
        },
        {
          id: '3',
          name: 'Predictive Oracle',
          type: 'predictor',
          status: 'training',
          capabilities: ['Time Series Forecasting', 'Risk Assessment', 'Market Prediction'],
          performance: {
            accuracy: 0.91,
            speed: 0.85,
            efficiency: 0.89
          },
          usage: {
            totalTasks: 634,
            successRate: 0.91,
            avgResponseTime: 3.7
          },
          description: 'Predictive AI agent with quantum-enhanced forecasting capabilities',
          lastActive: new Date(Date.now() - 1800000).toISOString(),
          version: '4.1.0'
        },
        {
          id: '4',
          name: 'Content Generator',
          type: 'generator',
          status: 'idle',
          capabilities: ['Text Generation', 'Code Synthesis', 'Creative Writing'],
          performance: {
            accuracy: 0.86,
            speed: 0.94,
            efficiency: 0.87
          },
          usage: {
            totalTasks: 423,
            successRate: 0.89,
            avgResponseTime: 1.8
          },
          description: 'Creative AI agent for generating high-quality content and code',
          lastActive: new Date(Date.now() - 3600000).toISOString(),
          version: '1.9.2'
        }
      ];
      
      // Mock tasks data
      const mockTasks: AITask[] = [
        {
          id: '1',
          title: 'Quantum Circuit Optimization',
          type: 'optimization',
          status: 'running',
          progress: 0.67,
          assignedAgent: 'Neural Optimizer',
          createdAt: new Date(Date.now() - 1800000).toISOString(),
          estimatedCompletion: new Date(Date.now() + 900000).toISOString(),
          priority: 'high'
        },
        {
          id: '2',
          title: 'Market Trend Analysis',
          type: 'analysis',
          status: 'completed',
          progress: 1.0,
          assignedAgent: 'Quantum Analyst',
          createdAt: new Date(Date.now() - 7200000).toISOString(),
          estimatedCompletion: new Date(Date.now() - 3600000).toISOString(),
          priority: 'medium'
        },
        {
          id: '3',
          title: 'Risk Prediction Model',
          type: 'prediction',
          status: 'pending',
          progress: 0,
          assignedAgent: 'Predictive Oracle',
          createdAt: new Date(Date.now() - 900000).toISOString(),
          estimatedCompletion: new Date(Date.now() + 3600000).toISOString(),
          priority: 'critical'
        },
        {
          id: '4',
          title: 'Documentation Generation',
          type: 'generation',
          status: 'failed',
          progress: 0.23,
          assignedAgent: 'Content Generator',
          createdAt: new Date(Date.now() - 5400000).toISOString(),
          estimatedCompletion: new Date(Date.now() - 1800000).toISOString(),
          priority: 'low'
        }
      ];
      
      setAgents(mockAgents);
      setTasks(mockTasks);
    } catch (error) {
      console.error('Load data error:', error);
      Alert.alert('Error', 'Failed to load FlyFox AI data');
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
      case 'training':
      case 'pending':
        return theme.colors.tertiary;
      case 'idle':
        return theme.colors.outline;
      case 'offline':
      case 'failed':
        return theme.colors.error;
      default:
        return theme.colors.outline;
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'assistant':
        return 'robot';
      case 'analyzer':
        return 'chart-line';
      case 'optimizer':
        return 'tune';
      case 'predictor':
        return 'crystal-ball';
      case 'generator':
        return 'creation';
      case 'analysis':
        return 'magnify';
      case 'optimization':
        return 'cog';
      case 'prediction':
        return 'trending-up';
      case 'generation':
        return 'file-document-plus';
      default:
        return 'help-circle';
    }
  };

  const getPriorityColor = (priority: AITask['priority']) => {
    switch (priority) {
      case 'critical':
        return '#F44336';
      case 'high':
        return '#FF9800';
      case 'medium':
        return '#2196F3';
      case 'low':
        return '#4CAF50';
      default:
        return theme.colors.outline;
    }
  };

  const handleAgentPress = (agent: AIAgent) => {
    navigation.navigate('AgentDetails', { agentId: agent.id });
  };

  const handleTaskPress = (task: AITask) => {
    navigation.navigate('TaskDetails', { taskId: task.id });
  };

  const handleCreateTask = () => {
    navigation.navigate('CreateAITask');
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    
    if (diffMinutes < 1) {
      return 'Just now';
    } else if (diffMinutes < 60) {
      return `${diffMinutes}m ago`;
    } else if (diffMinutes < 1440) {
      return `${Math.floor(diffMinutes / 60)}h ago`;
    } else {
      return `${Math.floor(diffMinutes / 1440)}d ago`;
    }
  };

  const formatEstimatedTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    
    if (diffMinutes < 0) {
      return 'Overdue';
    } else if (diffMinutes < 60) {
      return `${diffMinutes}m remaining`;
    } else if (diffMinutes < 1440) {
      return `${Math.floor(diffMinutes / 60)}h remaining`;
    } else {
      return `${Math.floor(diffMinutes / 1440)}d remaining`;
    }
  };

  if (isLoading && agents.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading FlyFox AI..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>FlyFox AI Platform</Title>
        <Paragraph style={styles.subtitle}>
          Manage your intelligent AI agents and automated tasks
        </Paragraph>
        
        <View style={styles.tabContainer}>
          <Button
            mode={activeTab === 'agents' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('agents')}
            style={styles.tabButton}
          >
            AI Agents
          </Button>
          <Button
            mode={activeTab === 'tasks' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('tasks')}
            style={styles.tabButton}
          >
            Active Tasks
          </Button>
        </View>
      </Surface>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'agents' ? (
          agents.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="robot" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No AI Agents</Title>
                <Paragraph style={styles.emptyText}>
                  Deploy your first AI agent to get started
                </Paragraph>
              </Card.Content>
            </Card>
          ) : (
            agents.map((agent) => (
              <Card 
                key={agent.id} 
                style={styles.agentCard}
                onPress={() => handleAgentPress(agent)}
              >
                <Card.Content>
                  <View style={styles.agentHeader}>
                    <View style={styles.agentInfo}>
                      <View style={styles.agentTitleRow}>
                        <Icon 
                          name={getTypeIcon(agent.type)} 
                          size={24} 
                          color={theme.colors.primary} 
                        />
                        <Text style={styles.agentName}>{agent.name}</Text>
                        <Text style={[styles.versionBadge, { backgroundColor: theme.colors.primaryContainer, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, fontSize: 12 }]}>v{Array.isArray(agent.version) ? agent.version.join('.') : agent.version}</Text>
                      </View>
                      <Text style={styles.agentDescription}>
                        {agent.description}
                      </Text>
                    </View>
                    <Chip 
                      style={[styles.statusChip, { backgroundColor: getStatusColor(agent.status) }]}
                      textStyle={{ color: theme.colors.onPrimary }}
                    >
                      {agent.status}
                    </Chip>
                  </View>

                  <View style={styles.performanceContainer}>
                    <Text style={styles.performanceTitle}>Performance Metrics</Text>
                    <View style={styles.metricsGrid}>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Accuracy</Text>
                        <ProgressBar 
                          progress={agent.performance.accuracy} 
                          color={theme.colors.primary}
                          style={styles.metricBar}
                        />
                        <Text style={styles.metricValue}>{Math.round(agent.performance.accuracy * 100)}%</Text>
                      </View>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Speed</Text>
                        <ProgressBar 
                          progress={agent.performance.speed} 
                          color={theme.colors.secondary}
                          style={styles.metricBar}
                        />
                        <Text style={styles.metricValue}>{Math.round(agent.performance.speed * 100)}%</Text>
                      </View>
                      <View style={styles.metricItem}>
                        <Text style={styles.metricLabel}>Efficiency</Text>
                        <ProgressBar 
                          progress={agent.performance.efficiency} 
                          color={theme.colors.tertiary}
                          style={styles.metricBar}
                        />
                        <Text style={styles.metricValue}>{Math.round(agent.performance.efficiency * 100)}%</Text>
                      </View>
                    </View>
                  </View>

                  <Divider style={styles.divider} />

                  <View style={styles.agentStats}>
                    <View style={styles.statItem}>
                      <Icon name="check-circle" size={16} color={theme.colors.primary} />
                      <Text style={styles.statText}>{agent.usage.totalTasks} tasks</Text>
                    </View>
                    <View style={styles.statItem}>
                      <Icon name="percent" size={16} color={theme.colors.tertiary} />
                      <Text style={styles.statText}>{Math.round(agent.usage.successRate * 100)}% success</Text>
                    </View>
                    <View style={styles.statItem}>
                      <Icon name="clock" size={16} color={theme.colors.outline} />
                      <Text style={styles.statText}>{agent.usage.avgResponseTime}s avg</Text>
                    </View>
                  </View>

                  <View style={styles.capabilitiesContainer}>
                    <Text style={styles.capabilitiesTitle}>Capabilities:</Text>
                    <View style={styles.capabilitiesList}>
                      {agent.capabilities.map((capability, index) => (
                        <Chip key={index} style={styles.capabilityChip} compact>
                          {capability}
                        </Chip>
                      ))}
                    </View>
                  </View>

                  <Text style={styles.lastActiveText}>
                    Last active: {formatTime(agent.lastActive)}
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        ) : (
          tasks.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="clipboard-list" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Active Tasks</Title>
                <Paragraph style={styles.emptyText}>
                  Create a new task to get started
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreateTask}
                  style={styles.createButton}
                >
                  Create Task
                </Button>
              </Card.Content>
            </Card>
          ) : (
            tasks.map((task) => (
              <Card 
                key={task.id} 
                style={styles.taskCard}
                onPress={() => handleTaskPress(task)}
              >
                <Card.Content>
                  <View style={styles.taskHeader}>
                    <View style={styles.taskInfo}>
                      <View style={styles.taskTitleRow}>
                        <Icon 
                          name={getTypeIcon(task.type)} 
                          size={20} 
                          color={theme.colors.primary} 
                        />
                        <Text style={styles.taskTitle}>{task.title}</Text>
                      </View>
                      <Text style={styles.taskAgent}>Assigned to: {task.assignedAgent}</Text>
                    </View>
                    <View style={styles.taskBadges}>
                      <Chip 
                        style={[styles.priorityChip, { backgroundColor: getPriorityColor(task.priority) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {task.priority}
                      </Chip>
                      <Chip 
                        style={[styles.statusChip, { backgroundColor: getStatusColor(task.status) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {task.status}
                      </Chip>
                    </View>
                  </View>

                  {task.status === 'running' && (
                    <View style={styles.progressContainer}>
                      <View style={styles.progressHeader}>
                        <Text style={styles.progressText}>Progress</Text>
                        <Text style={styles.progressPercentage}>
                          {Math.round(task.progress * 100)}%
                        </Text>
                      </View>
                      <ProgressBar 
                        progress={task.progress} 
                        color={theme.colors.primary}
                        style={styles.progressBar}
                      />
                    </View>
                  )}

                  <View style={styles.taskFooter}>
                    <Text style={styles.taskTime}>
                      Created: {formatTime(task.createdAt)}
                    </Text>
                    <Text style={styles.taskEstimate}>
                      {task.status === 'completed' ? 'Completed' : formatEstimatedTime(task.estimatedCompletion)}
                    </Text>
                  </View>
                </Card.Content>
              </Card>
            ))
          )
        )}
      </ScrollView>

      {activeTab === 'tasks' && (
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={handleCreateTask}
          label="New Task"
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
  agentCard: {
    marginBottom: 16,
    elevation: 2,
  },
  agentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  agentInfo: {
    flex: 1,
    marginRight: 12,
  },
  agentTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  agentName: {
    fontSize: 18,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginLeft: 8,
    marginRight: 8,
  },
  versionBadge: {
    height: 20,
  },
  agentDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 20,
  },
  statusChip: {
    height: 28,
  },
  performanceContainer: {
    marginBottom: 16,
  },
  performanceTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  metricsGrid: {
    gap: 8,
  },
  metricItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  metricLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 60,
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
    width: 35,
    textAlign: 'right',
  },
  divider: {
    marginVertical: 12,
  },
  agentStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 12,
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
  capabilitiesContainer: {
    marginBottom: 12,
  },
  capabilitiesTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  capabilitiesList: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  capabilityChip: {
    marginRight: 6,
    marginBottom: 4,
    backgroundColor: theme.colors.surfaceVariant,
  },
  lastActiveText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  taskCard: {
    marginBottom: 12,
    elevation: 2,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  taskInfo: {
    flex: 1,
    marginRight: 12,
  },
  taskTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginLeft: 8,
  },
  taskAgent: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  taskBadges: {
    gap: 4,
  },
  priorityChip: {
    height: 24,
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
  taskFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  taskTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  taskEstimate: {
    fontSize: 12,
    color: theme.colors.primary,
    fontWeight: '600',
  },
  fab: {
    position: 'absolute',
    margin: 16,
    right: 0,
    bottom: 0,
    backgroundColor: theme.colors.primary,
  },
});

export default FlyFoxAIScreen;