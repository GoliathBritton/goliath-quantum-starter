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
  DataTable,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
// import { LineChart, BarChart } from 'react-native-chart-kit'; // Removed for compatibility

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface GoliathTradeScreenProps {
  navigation: any;
}

interface TradingPosition {
  id: string;
  symbol: string;
  type: 'long' | 'short';
  size: number;
  entryPrice: number;
  currentPrice: number;
  pnl: number;
  pnlPercentage: number;
  openTime: string;
  status: 'open' | 'closed' | 'pending';
  strategy: string;
  riskLevel: 'low' | 'medium' | 'high';
}

interface TradingStrategy {
  id: string;
  name: string;
  description: string;
  performance: {
    totalTrades: number;
    winRate: number;
    avgReturn: number;
    sharpeRatio: number;
    maxDrawdown: number;
  };
  status: 'active' | 'paused' | 'stopped';
  riskLevel: 'conservative' | 'moderate' | 'aggressive';
  allocation: number;
  lastUpdated: string;
}

interface MarketData {
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  volume: number;
  high24h: number;
  low24h: number;
  marketCap: number;
}

const GoliathTradeScreen: React.FC<GoliathTradeScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [positions, setPositions] = useState<TradingPosition[]>([]);
  const [strategies, setStrategies] = useState<TradingStrategy[]>([]);
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [activeTab, setActiveTab] = useState<'positions' | 'strategies' | 'market'>('positions');
  const [portfolioValue, setPortfolioValue] = useState(0);
  const [totalPnL, setTotalPnL] = useState(0);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock positions data
      const mockPositions: TradingPosition[] = [
        {
          id: '1',
          symbol: 'BTC/USD',
          type: 'long',
          size: 0.5,
          entryPrice: 42500,
          currentPrice: 43200,
          pnl: 350,
          pnlPercentage: 1.65,
          openTime: new Date(Date.now() - 3600000).toISOString(),
          status: 'open',
          strategy: 'Quantum Momentum',
          riskLevel: 'medium'
        },
        {
          id: '2',
          symbol: 'ETH/USD',
          type: 'short',
          size: 2.0,
          entryPrice: 2650,
          currentPrice: 2580,
          pnl: 140,
          pnlPercentage: 2.64,
          openTime: new Date(Date.now() - 7200000).toISOString(),
          status: 'open',
          strategy: 'Neural Arbitrage',
          riskLevel: 'high'
        },
        {
          id: '3',
          symbol: 'SOL/USD',
          type: 'long',
          size: 10,
          entryPrice: 95.50,
          currentPrice: 92.30,
          pnl: -32,
          pnlPercentage: -3.35,
          openTime: new Date(Date.now() - 1800000).toISOString(),
          status: 'open',
          strategy: 'Quantum Reversal',
          riskLevel: 'low'
        }
      ];
      
      // Mock strategies data
      const mockStrategies: TradingStrategy[] = [
        {
          id: '1',
          name: 'Quantum Momentum',
          description: 'Advanced momentum trading using quantum algorithms',
          performance: {
            totalTrades: 247,
            winRate: 0.68,
            avgReturn: 0.034,
            sharpeRatio: 1.85,
            maxDrawdown: 0.12
          },
          status: 'active',
          riskLevel: 'moderate',
          allocation: 0.35,
          lastUpdated: new Date().toISOString()
        },
        {
          id: '2',
          name: 'Neural Arbitrage',
          description: 'AI-powered arbitrage opportunities across exchanges',
          performance: {
            totalTrades: 1834,
            winRate: 0.89,
            avgReturn: 0.018,
            sharpeRatio: 2.34,
            maxDrawdown: 0.05
          },
          status: 'active',
          riskLevel: 'conservative',
          allocation: 0.25,
          lastUpdated: new Date(Date.now() - 300000).toISOString()
        },
        {
          id: '3',
          name: 'Quantum Reversal',
          description: 'Mean reversion strategy with quantum-enhanced signals',
          performance: {
            totalTrades: 156,
            winRate: 0.72,
            avgReturn: 0.045,
            sharpeRatio: 1.67,
            maxDrawdown: 0.18
          },
          status: 'paused',
          riskLevel: 'aggressive',
          allocation: 0.15,
          lastUpdated: new Date(Date.now() - 1800000).toISOString()
        },
        {
          id: '4',
          name: 'Volatility Harvester',
          description: 'Captures volatility premiums using advanced options strategies',
          performance: {
            totalTrades: 89,
            winRate: 0.76,
            avgReturn: 0.028,
            sharpeRatio: 1.92,
            maxDrawdown: 0.09
          },
          status: 'active',
          riskLevel: 'moderate',
          allocation: 0.25,
          lastUpdated: new Date(Date.now() - 600000).toISOString()
        }
      ];
      
      // Mock market data
      const mockMarketData: MarketData[] = [
        {
          symbol: 'BTC/USD',
          price: 43200,
          change: 850,
          changePercent: 2.01,
          volume: 28500000000,
          high24h: 43850,
          low24h: 41900,
          marketCap: 847000000000
        },
        {
          symbol: 'ETH/USD',
          price: 2580,
          change: -45,
          changePercent: -1.71,
          volume: 12300000000,
          high24h: 2650,
          low24h: 2520,
          marketCap: 310000000000
        },
        {
          symbol: 'SOL/USD',
          price: 92.30,
          change: 3.20,
          changePercent: 3.59,
          volume: 1800000000,
          high24h: 95.80,
          low24h: 88.50,
          marketCap: 42000000000
        },
        {
          symbol: 'ADA/USD',
          price: 0.485,
          change: 0.012,
          changePercent: 2.54,
          volume: 890000000,
          high24h: 0.492,
          low24h: 0.468,
          marketCap: 17200000000
        }
      ];
      
      setPositions(mockPositions);
      setStrategies(mockStrategies);
      setMarketData(mockMarketData);
      
      // Calculate portfolio metrics
      const totalPnL = mockPositions.reduce((sum, pos) => sum + pos.pnl, 0);
      setTotalPnL(totalPnL);
      setPortfolioValue(125000 + totalPnL); // Base portfolio value + PnL
      
    } catch (error) {
      console.error('Load data error:', error);
      Alert.alert('Error', 'Failed to load trading data');
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
      case 'open':
        return theme.colors.primary;
      case 'paused':
      case 'pending':
        return theme.colors.tertiary;
      case 'stopped':
      case 'closed':
        return theme.colors.outline;
      default:
        return theme.colors.outline;
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low':
      case 'conservative':
        return '#4CAF50';
      case 'medium':
      case 'moderate':
        return '#FF9800';
      case 'high':
      case 'aggressive':
        return '#F44336';
      default:
        return theme.colors.outline;
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatNumber = (value: number, decimals: number = 2) => {
    return new Intl.NumberFormat('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
  };

  const handlePositionPress = (position: TradingPosition) => {
    navigation.navigate('PositionDetails', { positionId: position.id });
  };

  const handleStrategyPress = (strategy: TradingStrategy) => {
    navigation.navigate('StrategyDetails', { strategyId: strategy.id });
  };

  const handleCreatePosition = () => {
    navigation.navigate('CreatePosition');
  };

  const handleCreateStrategy = () => {
    navigation.navigate('CreateStrategy');
  };

  if (isLoading && positions.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading Goliath Trade..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <Title style={styles.title}>Goliath Trade</Title>
        <Paragraph style={styles.subtitle}>
          Quantum-powered algorithmic trading platform
        </Paragraph>
        
        {/* Portfolio Summary */}
        <Card style={styles.summaryCard}>
          <Card.Content>
            <View style={styles.summaryRow}>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Portfolio Value</Text>
                <Text style={styles.summaryValue}>{formatCurrency(portfolioValue)}</Text>
              </View>
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Total P&L</Text>
                <Text style={[styles.summaryValue, { color: totalPnL >= 0 ? '#4CAF50' : '#F44336' }]}>
                  {formatCurrency(totalPnL)}
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>
        
        <View style={styles.tabContainer}>
          <Button
            mode={activeTab === 'positions' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('positions')}
            style={styles.tabButton}
            compact
          >
            Positions
          </Button>
          <Button
            mode={activeTab === 'strategies' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('strategies')}
            style={styles.tabButton}
            compact
          >
            Strategies
          </Button>
          <Button
            mode={activeTab === 'market' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('market')}
            style={styles.tabButton}
            compact
          >
            Market
          </Button>
        </View>
      </Surface>

      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {activeTab === 'positions' ? (
          positions.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="chart-line" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Open Positions</Title>
                <Paragraph style={styles.emptyText}>
                  Create your first trading position to get started
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreatePosition}
                  style={styles.createButton}
                >
                  Create Position
                </Button>
              </Card.Content>
            </Card>
          ) : (
            positions.map((position) => (
              <Card 
                key={position.id} 
                style={styles.positionCard}
                onPress={() => handlePositionPress(position)}
              >
                <Card.Content>
                  <View style={styles.positionHeader}>
                    <View style={styles.positionInfo}>
                      <Text style={styles.positionSymbol}>{position.symbol}</Text>
                      <View style={styles.positionMeta}>
                        <Chip 
                          style={[styles.typeChip, { 
                            backgroundColor: position.type === 'long' ? '#4CAF50' : '#F44336' 
                          }]}
                          textStyle={{ color: theme.colors.onPrimary }}
                          compact
                        >
                          {position.type.toUpperCase()}
                        </Chip>
                        <Chip 
                          style={[styles.riskChip, { backgroundColor: getRiskColor(position.riskLevel) }]}
                          textStyle={{ color: theme.colors.onPrimary }}
                          compact
                        >
                          {position.riskLevel}
                        </Chip>
                      </View>
                    </View>
                    <View style={styles.positionPnL}>
                      <Text style={[styles.pnlValue, { 
                        color: position.pnl >= 0 ? '#4CAF50' : '#F44336' 
                      }]}>
                        {formatCurrency(position.pnl)}
                      </Text>
                      <Text style={[styles.pnlPercentage, { 
                        color: position.pnl >= 0 ? '#4CAF50' : '#F44336' 
                      }]}>
                        {formatPercentage(position.pnlPercentage)}
                      </Text>
                    </View>
                  </View>

                  <Divider style={styles.divider} />

                  <View style={styles.positionDetails}>
                    <View style={styles.detailRow}>
                      <Text style={styles.detailLabel}>Size:</Text>
                      <Text style={styles.detailValue}>{formatNumber(position.size, 4)}</Text>
                    </View>
                    <View style={styles.detailRow}>
                      <Text style={styles.detailLabel}>Entry:</Text>
                      <Text style={styles.detailValue}>{formatCurrency(position.entryPrice)}</Text>
                    </View>
                    <View style={styles.detailRow}>
                      <Text style={styles.detailLabel}>Current:</Text>
                      <Text style={styles.detailValue}>{formatCurrency(position.currentPrice)}</Text>
                    </View>
                    <View style={styles.detailRow}>
                      <Text style={styles.detailLabel}>Strategy:</Text>
                      <Text style={styles.detailValue}>{position.strategy}</Text>
                    </View>
                  </View>

                  <Text style={styles.openTime}>
                    Opened: {new Date(position.openTime).toLocaleString()}
                  </Text>
                </Card.Content>
              </Card>
            ))
          )
        ) : activeTab === 'strategies' ? (
          strategies.length === 0 ? (
            <Card style={styles.emptyCard}>
              <Card.Content style={styles.emptyContent}>
                <Icon name="brain" size={64} color={theme.colors.outline} />
                <Title style={styles.emptyTitle}>No Trading Strategies</Title>
                <Paragraph style={styles.emptyText}>
                  Create your first trading strategy to get started
                </Paragraph>
                <Button 
                  mode="contained" 
                  onPress={handleCreateStrategy}
                  style={styles.createButton}
                >
                  Create Strategy
                </Button>
              </Card.Content>
            </Card>
          ) : (
            strategies.map((strategy) => (
              <Card 
                key={strategy.id} 
                style={styles.strategyCard}
                onPress={() => handleStrategyPress(strategy)}
              >
                <Card.Content>
                  <View style={styles.strategyHeader}>
                    <View style={styles.strategyInfo}>
                      <Text style={styles.strategyName}>{strategy.name}</Text>
                      <Text style={styles.strategyDescription}>{strategy.description}</Text>
                    </View>
                    <View style={styles.strategyBadges}>
                      <Chip 
                        style={[styles.statusChip, { backgroundColor: getStatusColor(strategy.status) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {strategy.status}
                      </Chip>
                      <Chip 
                        style={[styles.riskChip, { backgroundColor: getRiskColor(strategy.riskLevel) }]}
                        textStyle={{ color: theme.colors.onPrimary }}
                        compact
                      >
                        {strategy.riskLevel}
                      </Chip>
                    </View>
                  </View>

                  <View style={styles.performanceGrid}>
                    <View style={styles.performanceItem}>
                      <Text style={styles.performanceLabel}>Win Rate</Text>
                      <Text style={styles.performanceValue}>
                        {formatPercentage(strategy.performance.winRate * 100)}
                      </Text>
                    </View>
                    <View style={styles.performanceItem}>
                      <Text style={styles.performanceLabel}>Avg Return</Text>
                      <Text style={styles.performanceValue}>
                        {formatPercentage(strategy.performance.avgReturn * 100)}
                      </Text>
                    </View>
                    <View style={styles.performanceItem}>
                      <Text style={styles.performanceLabel}>Sharpe Ratio</Text>
                      <Text style={styles.performanceValue}>
                        {formatNumber(strategy.performance.sharpeRatio, 2)}
                      </Text>
                    </View>
                    <View style={styles.performanceItem}>
                      <Text style={styles.performanceLabel}>Max Drawdown</Text>
                      <Text style={styles.performanceValue}>
                        {formatPercentage(-strategy.performance.maxDrawdown * 100)}
                      </Text>
                    </View>
                  </View>

                  <Divider style={styles.divider} />

                  <View style={styles.strategyFooter}>
                    <View style={styles.allocationContainer}>
                      <Text style={styles.allocationLabel}>Allocation</Text>
                      <ProgressBar 
                        progress={strategy.allocation} 
                        color={theme.colors.primary}
                        style={styles.allocationBar}
                      />
                      <Text style={styles.allocationValue}>
                        {formatPercentage(strategy.allocation * 100)}
                      </Text>
                    </View>
                    <Text style={styles.lastUpdated}>
                      Updated: {new Date(strategy.lastUpdated).toLocaleString()}
                    </Text>
                  </View>
                </Card.Content>
              </Card>
            ))
          )
        ) : (
          <View>
            {marketData.map((market) => (
              <Card key={market.symbol} style={styles.marketCard}>
                <Card.Content>
                  <View style={styles.marketHeader}>
                    <Text style={styles.marketSymbol}>{market.symbol}</Text>
                    <View style={styles.marketPrice}>
                      <Text style={styles.priceValue}>{formatCurrency(market.price)}</Text>
                      <Text style={[styles.priceChange, { 
                        color: market.change >= 0 ? '#4CAF50' : '#F44336' 
                      }]}>
                        {formatPercentage(market.changePercent)}
                      </Text>
                    </View>
                  </View>
                  
                  <View style={styles.marketStats}>
                    <View style={styles.statItem}>
                      <Text style={styles.statLabel}>24h High</Text>
                      <Text style={styles.statValue}>{formatCurrency(market.high24h)}</Text>
                    </View>
                    <View style={styles.statItem}>
                      <Text style={styles.statLabel}>24h Low</Text>
                      <Text style={styles.statValue}>{formatCurrency(market.low24h)}</Text>
                    </View>
                    <View style={styles.statItem}>
                      <Text style={styles.statLabel}>Volume</Text>
                      <Text style={styles.statValue}>
                        {formatCurrency(market.volume / 1000000)}M
                      </Text>
                    </View>
                    <View style={styles.statItem}>
                      <Text style={styles.statLabel}>Market Cap</Text>
                      <Text style={styles.statValue}>
                        {formatCurrency(market.marketCap / 1000000000)}B
                      </Text>
                    </View>
                  </View>
                </Card.Content>
              </Card>
            ))}
          </View>
        )}
      </ScrollView>

      {(activeTab === 'positions' || activeTab === 'strategies') && (
        <FAB
          icon="plus"
          style={styles.fab}
          onPress={activeTab === 'positions' ? handleCreatePosition : handleCreateStrategy}
          label={activeTab === 'positions' ? 'New Position' : 'New Strategy'}
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
  summaryCard: {
    marginBottom: 16,
    backgroundColor: theme.colors.primaryContainer,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 4,
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
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
  positionCard: {
    marginBottom: 12,
    elevation: 2,
  },
  positionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  positionInfo: {
    flex: 1,
  },
  positionSymbol: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  positionMeta: {
    flexDirection: 'row',
    gap: 8,
  },
  typeChip: {
    height: 24,
  },
  riskChip: {
    height: 24,
  },
  positionPnL: {
    alignItems: 'flex-end',
  },
  pnlValue: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  pnlPercentage: {
    fontSize: 12,
    fontWeight: '600',
  },
  divider: {
    marginVertical: 12,
  },
  positionDetails: {
    gap: 4,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  detailLabel: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
  },
  openTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginTop: 8,
    fontStyle: 'italic',
  },
  strategyCard: {
    marginBottom: 12,
    elevation: 2,
  },
  strategyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  strategyInfo: {
    flex: 1,
    marginRight: 12,
  },
  strategyName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  strategyDescription: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 16,
  },
  strategyBadges: {
    gap: 4,
  },
  statusChip: {
    height: 24,
  },
  performanceGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 12,
  },
  performanceItem: {
    flex: 1,
    minWidth: '45%',
    alignItems: 'center',
  },
  performanceLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 4,
  },
  performanceValue: {
    fontSize: 14,
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
  strategyFooter: {
    gap: 8,
  },
  allocationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  allocationLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    width: 60,
  },
  allocationBar: {
    flex: 1,
    height: 6,
    borderRadius: 3,
  },
  allocationValue: {
    fontSize: 12,
    fontWeight: '600',
    color: theme.colors.onSurface,
    width: 40,
    textAlign: 'right',
  },
  lastUpdated: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    fontStyle: 'italic',
  },
  marketCard: {
    marginBottom: 12,
    elevation: 2,
  },
  marketHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  marketSymbol: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  marketPrice: {
    alignItems: 'flex-end',
  },
  priceValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  priceChange: {
    fontSize: 12,
    fontWeight: '600',
  },
  marketStats: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statItem: {
    flex: 1,
    minWidth: '45%',
  },
  statLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 2,
  },
  statValue: {
    fontSize: 14,
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

export default GoliathTradeScreen;