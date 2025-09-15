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
  Searchbar,
  Badge,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface SigmaSelectScreenProps {
  navigation: any;
}

interface SigmaModel {
  id: string;
  name: string;
  version: string;
  category: 'classification' | 'regression' | 'clustering' | 'nlp' | 'computer_vision';
  accuracy: number;
  size: string;
  description: string;
  features: string[];
  status: 'available' | 'training' | 'deprecated';
  lastUpdated: string;
  downloads: number;
  rating: number;
  complexity: 'low' | 'medium' | 'high';
}

const SigmaSelectScreen: React.FC<SigmaSelectScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [models, setModels] = useState<SigmaModel[]>([]);
  const [filteredModels, setFilteredModels] = useState<SigmaModel[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedComplexity, setSelectedComplexity] = useState<string>('all');

  const categories = ['all', 'classification', 'regression', 'clustering', 'nlp', 'computer_vision'];
  const complexities = ['all', 'low', 'medium', 'high'];

  useEffect(() => {
    loadModels();
  }, []);

  useEffect(() => {
    filterModels();
  }, [models, searchQuery, selectedCategory, selectedComplexity]);

  const loadModels = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock data
      const mockModels: SigmaModel[] = [
        {
          id: '1',
          name: 'Sigma Neural Classifier',
          version: '2.1.0',
          category: 'classification',
          accuracy: 0.94,
          size: '45.2 MB',
          description: 'Advanced neural network for multi-class classification with quantum-enhanced features',
          features: ['Multi-class support', 'Quantum enhancement', 'Real-time inference'],
          status: 'available',
          lastUpdated: new Date().toISOString(),
          downloads: 15420,
          rating: 4.8,
          complexity: 'medium'
        },
        {
          id: '2',
          name: 'Quantum Regression Model',
          version: '1.5.2',
          category: 'regression',
          accuracy: 0.89,
          size: '32.1 MB',
          description: 'Quantum-powered regression model for continuous value prediction',
          features: ['Quantum algorithms', 'High precision', 'Scalable architecture'],
          status: 'available',
          lastUpdated: new Date(Date.now() - 86400000).toISOString(),
          downloads: 8930,
          rating: 4.6,
          complexity: 'high'
        },
        {
          id: '3',
          name: 'Sigma Cluster Engine',
          version: '3.0.1',
          category: 'clustering',
          accuracy: 0.91,
          size: '28.7 MB',
          description: 'Unsupervised clustering with quantum-inspired optimization',
          features: ['K-means++', 'Quantum optimization', 'Auto-tuning'],
          status: 'available',
          lastUpdated: new Date(Date.now() - 172800000).toISOString(),
          downloads: 12350,
          rating: 4.7,
          complexity: 'low'
        },
        {
          id: '4',
          name: 'NLP Transformer Sigma',
          version: '4.2.0',
          category: 'nlp',
          accuracy: 0.96,
          size: '156.8 MB',
          description: 'State-of-the-art transformer model for natural language processing',
          features: ['BERT-based', 'Multi-language', 'Fine-tuning ready'],
          status: 'training',
          lastUpdated: new Date(Date.now() - 259200000).toISOString(),
          downloads: 23100,
          rating: 4.9,
          complexity: 'high'
        },
        {
          id: '5',
          name: 'Vision Sigma CNN',
          version: '2.8.3',
          category: 'computer_vision',
          accuracy: 0.93,
          size: '89.4 MB',
          description: 'Convolutional neural network optimized for computer vision tasks',
          features: ['ResNet architecture', 'Transfer learning', 'Real-time processing'],
          status: 'available',
          lastUpdated: new Date(Date.now() - 345600000).toISOString(),
          downloads: 18750,
          rating: 4.5,
          complexity: 'medium'
        }
      ];
      
      setModels(mockModels);
    } catch (error) {
      console.error('Load models error:', error);
      Alert.alert('Error', 'Failed to load Sigma models');
    } finally {
      setIsLoading(false);
    }
  };

  const filterModels = () => {
    let filtered = models;
    
    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(model => 
        model.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        model.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        model.features.some(feature => feature.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }
    
    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(model => model.category === selectedCategory);
    }
    
    // Filter by complexity
    if (selectedComplexity !== 'all') {
      filtered = filtered.filter(model => model.complexity === selectedComplexity);
    }
    
    setFilteredModels(filtered);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadModels();
    setRefreshing(false);
  };

  const getCategoryColor = (category: SigmaModel['category']) => {
    switch (category) {
      case 'classification':
        return theme.colors.primary;
      case 'regression':
        return theme.colors.secondary;
      case 'clustering':
        return theme.colors.tertiary;
      case 'nlp':
        return '#9C27B0';
      case 'computer_vision':
        return '#FF5722';
      default:
        return theme.colors.outline;
    }
  };

  const getComplexityColor = (complexity: SigmaModel['complexity']) => {
    switch (complexity) {
      case 'low':
        return '#4CAF50';
      case 'medium':
        return '#FF9800';
      case 'high':
        return '#F44336';
      default:
        return theme.colors.outline;
    }
  };

  const getStatusIcon = (status: SigmaModel['status']) => {
    switch (status) {
      case 'available':
        return 'check-circle';
      case 'training':
        return 'clock';
      case 'deprecated':
        return 'alert-circle';
      default:
        return 'help-circle';
    }
  };

  const handleModelSelect = (model: SigmaModel) => {
    if (model.status === 'available') {
      Alert.alert(
        'Select Model',
        `Do you want to use ${model.name} for your project?`,
        [
          {
            text: 'Cancel',
            style: 'cancel',
          },
          {
            text: 'Select',
            onPress: () => {
              // Navigate to model configuration or deployment
              navigation.navigate('ModelConfiguration', { modelId: model.id });
            },
          },
        ]
      );
    } else {
      Alert.alert('Model Unavailable', 'This model is currently not available for selection.');
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  if (isLoading && models.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading Sigma models..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>Sigma Model Selection</Title>
        <Paragraph style={styles.subtitle}>
          Choose the perfect AI model for your quantum-enhanced applications
        </Paragraph>
        
        <Searchbar
          placeholder="Search algorithms..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchBar}
        />
        
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          style={styles.filterContainer}
        >
          <Text style={styles.filterLabel}>Category:</Text>
          {categories.map((category) => (
            <Chip
              key={category}
              selected={selectedCategory === category}
              onPress={() => setSelectedCategory(category)}
              style={styles.filterChip}
              textStyle={{
                color: selectedCategory === category ? theme.colors.onPrimary : theme.colors.onSurface
              }}
            >
              {category.charAt(0).toUpperCase() + category.slice(1).replace('_', ' ')}
            </Chip>
          ))}
        </ScrollView>
        
        <ScrollView 
          horizontal 
          showsHorizontalScrollIndicator={false}
          style={styles.filterContainer}
        >
          <Text style={styles.filterLabel}>Complexity:</Text>
          {complexities.map((complexity) => (
            <Chip
              key={complexity}
              selected={selectedComplexity === complexity}
              onPress={() => setSelectedComplexity(complexity)}
              style={styles.filterChip}
              textStyle={{
                color: selectedComplexity === complexity ? theme.colors.onPrimary : theme.colors.onSurface
              }}
            >
              {complexity.charAt(0).toUpperCase() + complexity.slice(1)}
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
        {filteredModels.length === 0 ? (
          <Card style={styles.emptyCard}>
            <Card.Content style={styles.emptyContent}>
              <Icon name="robot" size={64} color={theme.colors.outline} />
              <Title style={styles.emptyTitle}>No Models Found</Title>
              <Paragraph style={styles.emptyText}>
                {searchQuery || selectedCategory !== 'all' || selectedComplexity !== 'all'
                  ? 'Try adjusting your search criteria'
                  : 'No Sigma models are currently available'
                }
              </Paragraph>
            </Card.Content>
          </Card>
        ) : (
          filteredModels.map((model) => (
            <Card 
              key={model.id} 
              style={styles.modelCard}
              onPress={() => handleModelSelect(model)}
            >
              <Card.Content>
                <View style={styles.modelHeader}>
                  <View style={styles.modelInfo}>
                    <View style={styles.modelTitleRow}>
                      <Text style={styles.modelName}>{model.name}</Text>
                      <Text style={[styles.versionBadge, { backgroundColor: theme.colors.primaryContainer, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, fontSize: 12 }]}>v{model.version}</Text>
                    </View>
                    <Text style={styles.modelDescription}>
                      {model.description}
                    </Text>
                  </View>
                  <Icon 
                    name={getStatusIcon(model.status)} 
                    size={24} 
                    color={model.status === 'available' ? theme.colors.primary : theme.colors.outline}
                  />
                </View>

                <View style={styles.modelTags}>
                  <Chip 
                    style={[styles.categoryChip, { backgroundColor: getCategoryColor(model.category) }]}
                    textStyle={{ color: theme.colors.onPrimary }}
                  >
                    {model.category.replace('_', ' ')}
                  </Chip>
                  <Chip 
                    style={[styles.complexityChip, { backgroundColor: getComplexityColor(model.complexity) }]}
                    textStyle={{ color: theme.colors.onPrimary }}
                  >
                    {model.complexity}
                  </Chip>
                </View>

                <View style={styles.modelMetrics}>
                  <View style={styles.metricItem}>
                    <Icon name="target" size={16} color={theme.colors.primary} />
                    <Text style={styles.metricText}>{Math.round(model.accuracy * 100)}% accuracy</Text>
                  </View>
                  <View style={styles.metricItem}>
                    <Icon name="download" size={16} color={theme.colors.outline} />
                    <Text style={styles.metricText}>{formatNumber(model.downloads)} downloads</Text>
                  </View>
                  <View style={styles.metricItem}>
                    <Icon name="star" size={16} color={theme.colors.tertiary} />
                    <Text style={styles.metricText}>{model.rating}/5</Text>
                  </View>
                </View>

                <Divider style={styles.divider} />

                <View style={styles.modelFooter}>
                  <View style={styles.modelDetails}>
                    <Text style={styles.detailText}>Size: {model.size}</Text>
                    <Text style={styles.detailText}>Updated: {formatDate(model.lastUpdated)}</Text>
                  </View>
                  <Button 
                    mode={model.status === 'available' ? 'contained' : 'outlined'}
                    disabled={model.status !== 'available'}
                    onPress={() => handleModelSelect(model)}
                    style={styles.selectButton}
                  >
                    {model.status === 'available' ? 'Select' : model.status}
                  </Button>
                </View>

                <View style={styles.featuresList}>
                  <Text style={styles.featuresTitle}>Key Features:</Text>
                  <View style={styles.featuresContainer}>
                    {model.features.map((feature, index) => (
                      <Chip key={index} style={styles.featureChip} compact>
                        {feature}
                      </Chip>
                    ))}
                  </View>
                </View>
              </Card.Content>
            </Card>
          ))
        )}
      </ScrollView>
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
  searchBar: {
    marginBottom: 16,
  },
  filterContainer: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  filterLabel: {
    fontSize: 14,
    color: theme.colors.onSurface,
    alignSelf: 'center',
    marginRight: 8,
    fontWeight: '600',
  },
  filterChip: {
    marginRight: 8,
    height: 32,
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
    opacity: 0.7,
  },
  modelCard: {
    marginBottom: 16,
    elevation: 2,
  },
  modelHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  modelInfo: {
    flex: 1,
    marginRight: 12,
  },
  modelTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  modelName: {
    fontSize: 18,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginRight: 8,
  },
  versionBadge: {
    height: 20,
  },
  modelDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 20,
  },
  modelTags: {
    flexDirection: 'row',
    marginBottom: 12,
  },
  categoryChip: {
    marginRight: 8,
    height: 28,
  },
  complexityChip: {
    height: 28,
  },
  modelMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  metricItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metricText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    marginLeft: 4,
  },
  divider: {
    marginVertical: 12,
  },
  modelFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  modelDetails: {
    flex: 1,
  },
  detailText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  selectButton: {
    backgroundColor: theme.colors.primary,
  },
  featuresList: {
    marginTop: 8,
  },
  featuresTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  featuresContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  featureChip: {
    marginRight: 6,
    marginBottom: 4,
    backgroundColor: theme.colors.surfaceVariant,
  },
});

export default SigmaSelectScreen;