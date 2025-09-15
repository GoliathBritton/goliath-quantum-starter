import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  Switch,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  List,
  Divider,
  Surface,
  Text,
  Chip,
  // Slider, // Not available in react-native-paper
  RadioButton,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface NotificationsScreenProps {
  navigation: any;
}

interface NotificationSetting {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  type: 'toggle' | 'time' | 'frequency';
  value: boolean | string | number;
  options?: string[];
  onToggle?: (value: boolean) => void;
  onValueChange?: (value: string | number) => void;
  category: 'system' | 'trading' | 'quantum' | 'social' | 'security';
}

interface NotificationHistory {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'warning' | 'error' | 'success';
  category: string;
  timestamp: string;
  read: boolean;
  actionRequired?: boolean;
}

const NotificationsScreen: React.FC<NotificationsScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'settings' | 'history'>('settings');
  const [notificationHistory, setNotificationHistory] = useState<NotificationHistory[]>([]);
  
  const [notificationSettings, setNotificationSettings] = useState({
    // System Notifications
    systemUpdates: true,
    maintenanceAlerts: true,
    errorNotifications: true,
    performanceAlerts: false,
    
    // Trading Notifications
    tradeExecutions: true,
    priceAlerts: true,
    portfolioUpdates: false,
    marketNews: true,
    riskAlerts: true,
    
    // Quantum Notifications
    quantumJobCompletion: true,
    circuitErrors: true,
    quantumAdvantageAlerts: false,
    coherenceWarnings: true,
    
    // Social Notifications
    teamUpdates: false,
    collaborationRequests: true,
    shareNotifications: false,
    
    // Security Notifications
    loginAlerts: true,
    securityWarnings: true,
    deviceChanges: true,
    suspiciousActivity: true,
    
    // Delivery Settings
    pushNotifications: true,
    emailNotifications: true,
    smsNotifications: false,
    inAppNotifications: true,
    
    // Timing Settings
    quietHoursEnabled: true,
    quietHoursStart: '22:00',
    quietHoursEnd: '08:00',
    weekendNotifications: false,
    
    // Frequency Settings
    digestFrequency: 'daily', // 'immediate', 'hourly', 'daily', 'weekly'
    maxNotificationsPerHour: 10,
  });

  useEffect(() => {
    loadNotificationData();
  }, []);

  const loadNotificationData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock notification history
      const mockHistory: NotificationHistory[] = [
        {
          id: '1',
          title: 'Quantum Job Completed',
          message: 'Your VQE optimization job has completed successfully with 94% fidelity.',
          type: 'success',
          category: 'Quantum',
          timestamp: new Date(Date.now() - 300000).toISOString(),
          read: false,
        },
        {
          id: '2',
          title: 'Trade Executed',
          message: 'Buy order for 100 shares of AAPL executed at $175.50.',
          type: 'info',
          category: 'Trading',
          timestamp: new Date(Date.now() - 900000).toISOString(),
          read: true,
        },
        {
          id: '3',
          title: 'Security Alert',
          message: 'New login detected from MacBook Pro in New York.',
          type: 'warning',
          category: 'Security',
          timestamp: new Date(Date.now() - 1800000).toISOString(),
          read: true,
          actionRequired: true,
        },
        {
          id: '4',
          title: 'System Maintenance',
          message: 'Scheduled maintenance will begin at 2:00 AM EST.',
          type: 'info',
          category: 'System',
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          read: true,
        },
        {
          id: '5',
          title: 'Quantum Circuit Error',
          message: 'Circuit execution failed due to decoherence. Please review your gates.',
          type: 'error',
          category: 'Quantum',
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          read: true,
        },
        {
          id: '6',
          title: 'Portfolio Alert',
          message: 'Your portfolio has gained 5.2% today. Consider rebalancing.',
          type: 'success',
          category: 'Trading',
          timestamp: new Date(Date.now() - 14400000).toISOString(),
          read: true,
        },
      ];
      
      setNotificationHistory(mockHistory);
      
    } catch (error) {
      console.error('Load notification data error:', error);
      Alert.alert('Error', 'Failed to load notification data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleSetting = (key: string, value: boolean) => {
    setNotificationSettings(prev => ({ ...prev, [key]: value }));
    saveSetting(key, value);
  };

  const handleValueChange = (key: string, value: string | number) => {
    setNotificationSettings(prev => ({ ...prev, [key]: value }));
    saveSetting(key, value);
  };

  const saveSetting = async (key: string, value: any) => {
    try {
      console.log(`Saving notification setting ${key}:`, value);
      // Save to API
    } catch (error) {
      console.error('Save setting error:', error);
      Alert.alert('Error', 'Failed to save setting');
    }
  };

  const handleMarkAsRead = (notificationId: string) => {
    setNotificationHistory(prev => 
      prev.map(notification => 
        notification.id === notificationId 
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const handleMarkAllAsRead = () => {
    setNotificationHistory(prev => 
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const handleClearHistory = () => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear all notification history?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: () => setNotificationHistory([]),
        },
      ]
    );
  };

  const getNotificationTypeColor = (type: string) => {
    switch (type) {
      case 'success':
        return theme.colors.primary;
      case 'warning':
        return '#FF9800';
      case 'error':
        return theme.colors.error;
      case 'info':
      default:
        return theme.colors.onSurface;
    }
  };

  const getNotificationTypeIcon = (type: string) => {
    switch (type) {
      case 'success':
        return 'check-circle';
      case 'warning':
        return 'alert';
      case 'error':
        return 'alert-circle';
      case 'info':
      default:
        return 'information';
    }
  };

  const notificationCategories = [
    {
      title: 'System Notifications',
      icon: 'cog',
      settings: [
        {
          id: 'systemUpdates',
          title: 'System Updates',
          subtitle: 'App updates and new features',
          icon: 'update',
          type: 'toggle' as const,
          value: notificationSettings.systemUpdates,
          onToggle: (value: boolean) => handleToggleSetting('systemUpdates', value),
          category: 'system' as const,
        },
        {
          id: 'maintenanceAlerts',
          title: 'Maintenance Alerts',
          subtitle: 'Scheduled maintenance notifications',
          icon: 'wrench',
          type: 'toggle' as const,
          value: notificationSettings.maintenanceAlerts,
          onToggle: (value: boolean) => handleToggleSetting('maintenanceAlerts', value),
          category: 'system' as const,
        },
        {
          id: 'errorNotifications',
          title: 'Error Notifications',
          subtitle: 'System errors and failures',
          icon: 'alert-circle',
          type: 'toggle' as const,
          value: notificationSettings.errorNotifications,
          onToggle: (value: boolean) => handleToggleSetting('errorNotifications', value),
          category: 'system' as const,
        },
        {
          id: 'performanceAlerts',
          title: 'Performance Alerts',
          subtitle: 'System performance warnings',
          icon: 'speedometer',
          type: 'toggle' as const,
          value: notificationSettings.performanceAlerts,
          onToggle: (value: boolean) => handleToggleSetting('performanceAlerts', value),
          category: 'system' as const,
        },
      ],
    },
    {
      title: 'Trading Notifications',
      icon: 'chart-line',
      settings: [
        {
          id: 'tradeExecutions',
          title: 'Trade Executions',
          subtitle: 'Buy and sell order confirmations',
          icon: 'swap-horizontal',
          type: 'toggle' as const,
          value: notificationSettings.tradeExecutions,
          onToggle: (value: boolean) => handleToggleSetting('tradeExecutions', value),
          category: 'trading' as const,
        },
        {
          id: 'priceAlerts',
          title: 'Price Alerts',
          subtitle: 'Asset price movement notifications',
          icon: 'trending-up',
          type: 'toggle' as const,
          value: notificationSettings.priceAlerts,
          onToggle: (value: boolean) => handleToggleSetting('priceAlerts', value),
          category: 'trading' as const,
        },
        {
          id: 'portfolioUpdates',
          title: 'Portfolio Updates',
          subtitle: 'Daily portfolio performance',
          icon: 'briefcase',
          type: 'toggle' as const,
          value: notificationSettings.portfolioUpdates,
          onToggle: (value: boolean) => handleToggleSetting('portfolioUpdates', value),
          category: 'trading' as const,
        },
        {
          id: 'marketNews',
          title: 'Market News',
          subtitle: 'Important market updates',
          icon: 'newspaper',
          type: 'toggle' as const,
          value: notificationSettings.marketNews,
          onToggle: (value: boolean) => handleToggleSetting('marketNews', value),
          category: 'trading' as const,
        },
        {
          id: 'riskAlerts',
          title: 'Risk Alerts',
          subtitle: 'Portfolio risk warnings',
          icon: 'shield-alert',
          type: 'toggle' as const,
          value: notificationSettings.riskAlerts,
          onToggle: (value: boolean) => handleToggleSetting('riskAlerts', value),
          category: 'trading' as const,
        },
      ],
    },
    {
      title: 'Quantum Notifications',
      icon: 'atom',
      settings: [
        {
          id: 'quantumJobCompletion',
          title: 'Job Completion',
          subtitle: 'Quantum job execution results',
          icon: 'check-circle',
          type: 'toggle' as const,
          value: notificationSettings.quantumJobCompletion,
          onToggle: (value: boolean) => handleToggleSetting('quantumJobCompletion', value),
          category: 'quantum' as const,
        },
        {
          id: 'circuitErrors',
          title: 'Circuit Errors',
          subtitle: 'Quantum circuit execution errors',
          icon: 'alert-circle',
          type: 'toggle' as const,
          value: notificationSettings.circuitErrors,
          onToggle: (value: boolean) => handleToggleSetting('circuitErrors', value),
          category: 'quantum' as const,
        },
        {
          id: 'quantumAdvantageAlerts',
          title: 'Quantum Advantage Alerts',
          subtitle: 'Quantum speedup opportunities',
          icon: 'rocket',
          type: 'toggle' as const,
          value: notificationSettings.quantumAdvantageAlerts,
          onToggle: (value: boolean) => handleToggleSetting('quantumAdvantageAlerts', value),
          category: 'quantum' as const,
        },
        {
          id: 'coherenceWarnings',
          title: 'Coherence Warnings',
          subtitle: 'Quantum coherence degradation',
          icon: 'wave',
          type: 'toggle' as const,
          value: notificationSettings.coherenceWarnings,
          onToggle: (value: boolean) => handleToggleSetting('coherenceWarnings', value),
          category: 'quantum' as const,
        },
      ],
    },
    {
      title: 'Security Notifications',
      icon: 'shield',
      settings: [
        {
          id: 'loginAlerts',
          title: 'Login Alerts',
          subtitle: 'New device login notifications',
          icon: 'login',
          type: 'toggle' as const,
          value: notificationSettings.loginAlerts,
          onToggle: (value: boolean) => handleToggleSetting('loginAlerts', value),
          category: 'security' as const,
        },
        {
          id: 'securityWarnings',
          title: 'Security Warnings',
          subtitle: 'Security threat notifications',
          icon: 'shield-alert',
          type: 'toggle' as const,
          value: notificationSettings.securityWarnings,
          onToggle: (value: boolean) => handleToggleSetting('securityWarnings', value),
          category: 'security' as const,
        },
        {
          id: 'deviceChanges',
          title: 'Device Changes',
          subtitle: 'Device registration changes',
          icon: 'devices',
          type: 'toggle' as const,
          value: notificationSettings.deviceChanges,
          onToggle: (value: boolean) => handleToggleSetting('deviceChanges', value),
          category: 'security' as const,
        },
        {
          id: 'suspiciousActivity',
          title: 'Suspicious Activity',
          subtitle: 'Unusual account activity',
          icon: 'eye-off',
          type: 'toggle' as const,
          value: notificationSettings.suspiciousActivity,
          onToggle: (value: boolean) => handleToggleSetting('suspiciousActivity', value),
          category: 'security' as const,
        },
      ],
    },
  ];

  if (isLoading && notificationHistory.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading notifications..."
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <View style={styles.tabContainer}>
          <Button
            mode={activeTab === 'settings' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('settings')}
            style={styles.tabButton}
            compact
          >
            Settings
          </Button>
          <Button
            mode={activeTab === 'history' ? 'contained' : 'outlined'}
            onPress={() => setActiveTab('history')}
            style={styles.tabButton}
            compact
          >
            History ({notificationHistory.filter(n => !n.read).length})
          </Button>
        </View>
      </Surface>

      <ScrollView style={styles.content}>
        {activeTab === 'settings' ? (
          <>
            {/* Delivery Methods */}
            <Card style={styles.sectionCard}>
              <Card.Content>
                <Text style={styles.sectionTitle}>Delivery Methods</Text>
                
                <List.Item
                  title="Push Notifications"
                  description="Receive notifications on your device"
                  left={(props) => <List.Icon {...props} icon="cellphone" />}
                  right={() => (
                    <Switch
                      value={notificationSettings.pushNotifications}
                      onValueChange={(value) => handleToggleSetting('pushNotifications', value)}
                    />
                  )}
                />
                <Divider style={styles.itemDivider} />
                
                <List.Item
                  title="Email Notifications"
                  description="Receive notifications via email"
                  left={(props) => <List.Icon {...props} icon="email" />}
                  right={() => (
                    <Switch
                      value={notificationSettings.emailNotifications}
                      onValueChange={(value) => handleToggleSetting('emailNotifications', value)}
                    />
                  )}
                />
                <Divider style={styles.itemDivider} />
                
                <List.Item
                  title="SMS Notifications"
                  description="Receive notifications via text message"
                  left={(props) => <List.Icon {...props} icon="message-text" />}
                  right={() => (
                    <Switch
                      value={notificationSettings.smsNotifications}
                      onValueChange={(value) => handleToggleSetting('smsNotifications', value)}
                    />
                  )}
                />
              </Card.Content>
            </Card>

            {/* Timing Settings */}
            <Card style={styles.sectionCard}>
              <Card.Content>
                <Text style={styles.sectionTitle}>Timing & Frequency</Text>
                
                <List.Item
                  title="Quiet Hours"
                  description={`${notificationSettings.quietHoursStart} - ${notificationSettings.quietHoursEnd}`}
                  left={(props) => <List.Icon {...props} icon="sleep" />}
                  right={() => (
                    <Switch
                      value={notificationSettings.quietHoursEnabled}
                      onValueChange={(value) => handleToggleSetting('quietHoursEnabled', value)}
                    />
                  )}
                />
                <Divider style={styles.itemDivider} />
                
                <List.Item
                  title="Weekend Notifications"
                  description="Receive notifications on weekends"
                  left={(props) => <List.Icon {...props} icon="calendar-weekend" />}
                  right={() => (
                    <Switch
                      value={notificationSettings.weekendNotifications}
                      onValueChange={(value) => handleToggleSetting('weekendNotifications', value)}
                    />
                  )}
                />
                <Divider style={styles.itemDivider} />
                
                <View style={styles.frequencyContainer}>
                  <Text style={styles.frequencyTitle}>Digest Frequency</Text>
                  <RadioButton.Group
                    onValueChange={(value) => handleValueChange('digestFrequency', value)}
                    value={notificationSettings.digestFrequency}
                  >
                    <View style={styles.radioOption}>
                      <RadioButton value="immediate" />
                      <Text style={styles.radioLabel}>Immediate</Text>
                    </View>
                    <View style={styles.radioOption}>
                      <RadioButton value="hourly" />
                      <Text style={styles.radioLabel}>Hourly</Text>
                    </View>
                    <View style={styles.radioOption}>
                      <RadioButton value="daily" />
                      <Text style={styles.radioLabel}>Daily</Text>
                    </View>
                    <View style={styles.radioOption}>
                      <RadioButton value="weekly" />
                      <Text style={styles.radioLabel}>Weekly</Text>
                    </View>
                  </RadioButton.Group>
                </View>
                
                <Divider style={styles.itemDivider} />
                
                <View style={styles.sliderContainer}>
                  <Text style={styles.sliderTitle}>
                    Max Notifications per Hour: {notificationSettings.maxNotificationsPerHour}
                  </Text>
                  <View style={styles.slider}>
                    <Button 
                      mode="outlined" 
                      onPress={() => handleValueChange('maxNotificationsPerHour', Math.max(1, notificationSettings.maxNotificationsPerHour - 1))}
                      disabled={notificationSettings.maxNotificationsPerHour <= 1}
                    >
                      -
                    </Button>
                    <Text style={{marginHorizontal: 16, fontSize: 16}}>{notificationSettings.maxNotificationsPerHour}</Text>
                    <Button 
                      mode="outlined" 
                      onPress={() => handleValueChange('maxNotificationsPerHour', Math.min(50, notificationSettings.maxNotificationsPerHour + 1))}
                      disabled={notificationSettings.maxNotificationsPerHour >= 50}
                    >
                      +
                    </Button>
                  </View>
                </View>
              </Card.Content>
            </Card>

            {/* Notification Categories */}
            {notificationCategories.map((category) => (
              <Card key={category.title} style={styles.sectionCard}>
                <Card.Content>
                  <View style={styles.categoryHeader}>
                    <Icon name={category.icon} size={20} color={theme.colors.primary} />
                    <Text style={styles.sectionTitle}>{category.title}</Text>
                  </View>
                  
                  {category.settings.map((setting, index) => (
                    <View key={setting.id}>
                      <List.Item
                        title={setting.title}
                        description={setting.subtitle}
                        left={(props) => <List.Icon {...props} icon={setting.icon} />}
                        right={() => (
                          <Switch
                            value={setting.value as boolean}
                            onValueChange={setting.onToggle}
                          />
                        )}
                        style={styles.listItem}
                      />
                      {index < category.settings.length - 1 && <Divider style={styles.itemDivider} />}
                    </View>
                  ))}
                </Card.Content>
              </Card>
            ))}
          </>
        ) : (
          <>
            {/* Notification History */}
            <Card style={styles.historyHeader}>
              <Card.Content>
                <View style={styles.historyActions}>
                  <Title style={styles.historyTitle}>Notification History</Title>
                  <View style={styles.historyButtons}>
                    <Button 
                      mode="outlined" 
                      compact 
                      onPress={handleMarkAllAsRead}
                      disabled={notificationHistory.every(n => n.read)}
                    >
                      Mark All Read
                    </Button>
                    <Button 
                      mode="outlined" 
                      compact 
                      onPress={handleClearHistory}
                      style={styles.clearButton}
                    >
                      Clear
                    </Button>
                  </View>
                </View>
              </Card.Content>
            </Card>

            {notificationHistory.length === 0 ? (
              <Card style={styles.emptyCard}>
                <Card.Content style={styles.emptyContent}>
                  <Icon name="bell-off" size={64} color={theme.colors.outline} />
                  <Title style={styles.emptyTitle}>No Notifications</Title>
                  <Paragraph style={styles.emptyText}>
                    You're all caught up! No notifications to show.
                  </Paragraph>
                </Card.Content>
              </Card>
            ) : (
              notificationHistory.map((notification) => (
                <Card 
                  key={notification.id} 
                  style={[
                    styles.notificationCard,
                    !notification.read && styles.unreadCard
                  ]}
                  onPress={() => handleMarkAsRead(notification.id)}
                >
                  <Card.Content>
                    <View style={styles.notificationHeader}>
                      <View style={styles.notificationIcon}>
                        <Icon 
                          name={getNotificationTypeIcon(notification.type)} 
                          size={20} 
                          color={getNotificationTypeColor(notification.type)}
                        />
                        {!notification.read && (
                          <View style={styles.unreadDot} />
                        )}
                      </View>
                      
                      <View style={styles.notificationContent}>
                        <View style={styles.notificationTitleRow}>
                          <Text style={styles.notificationTitle}>{notification.title}</Text>
                          <Chip 
                            style={styles.categoryChip}
                            textStyle={styles.categoryChipText}
                            compact
                          >
                            {notification.category}
                          </Chip>
                        </View>
                        <Text style={styles.notificationMessage}>{notification.message}</Text>
                        <Text style={styles.notificationTime}>
                          {new Date(notification.timestamp).toLocaleString()}
                        </Text>
                        
                        {notification.actionRequired && (
                          <Chip 
                            style={styles.actionChip}
                            textStyle={styles.actionChipText}
                            compact
                          >
                            Action Required
                          </Chip>
                        )}
                      </View>
                    </View>
                  </Card.Content>
                </Card>
              ))
            )}
          </>
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
    elevation: 2,
  },
  tabContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 8,
  },
  tabButton: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  sectionCard: {
    marginBottom: 16,
    elevation: 1,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.outline,
    opacity: 0.3,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  listItem: {
    paddingVertical: 8,
  },
  itemDivider: {
    marginVertical: 4,
    opacity: 0.3,
  },
  frequencyContainer: {
    marginVertical: 12,
  },
  frequencyTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  radioOption: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 4,
  },
  radioLabel: {
    fontSize: 14,
    color: theme.colors.onSurface,
    marginLeft: 8,
  },
  sliderContainer: {
    marginVertical: 12,
  },
  sliderTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  slider: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
  },
  historyHeader: {
    marginBottom: 16,
    elevation: 2,
  },
  historyActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  historyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
  },
  historyButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  clearButton: {
    borderColor: theme.colors.error,
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
  notificationCard: {
    marginBottom: 8,
    elevation: 1,
  },
  unreadCard: {
    borderLeftWidth: 4,
    borderLeftColor: theme.colors.primary,
    elevation: 2,
  },
  notificationHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  notificationIcon: {
    position: 'relative',
    marginRight: 12,
    marginTop: 2,
  },
  unreadDot: {
    position: 'absolute',
    top: -2,
    right: -2,
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: theme.colors.primary,
  },
  notificationContent: {
    flex: 1,
  },
  notificationTitleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  notificationTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    flex: 1,
    marginRight: 8,
  },
  categoryChip: {
    height: 20,
    backgroundColor: theme.colors.surfaceVariant,
  },
  categoryChipText: {
    fontSize: 10,
    color: theme.colors.onSurfaceVariant,
  },
  notificationMessage: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.8,
    lineHeight: 20,
    marginBottom: 8,
  },
  notificationTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.6,
    marginBottom: 8,
  },
  actionChip: {
    height: 24,
    backgroundColor: theme.colors.errorContainer,
    alignSelf: 'flex-start',
  },
  actionChipText: {
    fontSize: 12,
    color: theme.colors.onErrorContainer,
  },
});

export default NotificationsScreen;