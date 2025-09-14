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
  Avatar,
  IconButton,
  Chip,
  ProgressBar,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface SettingsScreenProps {
  navigation: any;
}

interface SettingsSection {
  id: string;
  title: string;
  icon: string;
  items: SettingsItem[];
}

interface SettingsItem {
  id: string;
  title: string;
  subtitle?: string;
  icon: string;
  type: 'navigation' | 'toggle' | 'action' | 'info';
  value?: boolean | string | number;
  onPress?: () => void;
  onToggle?: (value: boolean) => void;
  badge?: string;
  disabled?: boolean;
}

const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState({
    notifications: true,
    biometrics: false,
    darkMode: false,
    quantumMode: true,
    autoSync: true,
    analytics: false,
    crashReporting: true,
    betaFeatures: false,
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      setIsLoading(true);
      // Simulate API call to load user settings
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Load settings from storage or API
      // This would typically come from AsyncStorage or a settings API
      
    } catch (error) {
      console.error('Load settings error:', error);
      Alert.alert('Error', 'Failed to load settings');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleSetting = (key: string, value: boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }));
    // Save to storage or API
    saveSetting(key, value);
  };

  const saveSetting = async (key: string, value: any) => {
    try {
      // Save to AsyncStorage or API
      console.log(`Saving setting ${key}:`, value);
    } catch (error) {
      console.error('Save setting error:', error);
      Alert.alert('Error', 'Failed to save setting');
    }
  };

  const handleSignOut = () => {
    Alert.alert(
      'Sign Out',
      'Are you sure you want to sign out?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Sign Out',
          style: 'destructive',
          onPress: () => {
            // Dispatch sign out action
            navigation.navigate('Auth');
          },
        },
      ]
    );
  };

  const handleDeleteAccount = () => {
    Alert.alert(
      'Delete Account',
      'This action cannot be undone. All your data will be permanently deleted.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: () => {
            Alert.alert('Account Deletion', 'Please contact support to delete your account.');
          },
        },
      ]
    );
  };

  const settingsSections: SettingsSection[] = [
    {
      id: 'account',
      title: 'Account',
      icon: 'account',
      items: [
        {
          id: 'profile',
          title: 'Profile',
          subtitle: 'Edit your profile information',
          icon: 'account-edit',
          type: 'navigation',
          onPress: () => navigation.navigate('Profile'),
        },
        {
          id: 'security',
          title: 'Security',
          subtitle: 'Password, biometrics, and 2FA',
          icon: 'shield-account',
          type: 'navigation',
          onPress: () => navigation.navigate('Security'),
        },
        {
          id: 'privacy',
          title: 'Privacy',
          subtitle: 'Data usage and privacy controls',
          icon: 'eye-off',
          type: 'navigation',
          onPress: () => navigation.navigate('Privacy'),
        },
      ],
    },
    {
      id: 'preferences',
      title: 'Preferences',
      icon: 'cog',
      items: [
        {
          id: 'notifications',
          title: 'Notifications',
          subtitle: 'Push notifications and alerts',
          icon: 'bell',
          type: 'navigation',
          onPress: () => navigation.navigate('Notifications'),
          badge: settings.notifications ? 'On' : 'Off',
        },
        {
          id: 'darkMode',
          title: 'Dark Mode',
          subtitle: 'Use dark theme',
          icon: 'theme-light-dark',
          type: 'toggle',
          value: settings.darkMode,
          onToggle: (value) => handleToggleSetting('darkMode', value),
        },
        {
          id: 'quantumMode',
          title: 'Quantum Mode',
          subtitle: 'Enhanced quantum visualizations',
          icon: 'atom',
          type: 'toggle',
          value: settings.quantumMode,
          onToggle: (value) => handleToggleSetting('quantumMode', value),
        },
        {
          id: 'autoSync',
          title: 'Auto Sync',
          subtitle: 'Automatically sync data',
          icon: 'sync',
          type: 'toggle',
          value: settings.autoSync,
          onToggle: (value) => handleToggleSetting('autoSync', value),
        },
      ],
    },
    {
      id: 'data',
      title: 'Data & Storage',
      icon: 'database',
      items: [
        {
          id: 'storage',
          title: 'Storage Usage',
          subtitle: '2.3 GB of 10 GB used',
          icon: 'harddisk',
          type: 'navigation',
          onPress: () => navigation.navigate('Storage'),
        },
        {
          id: 'backup',
          title: 'Backup & Restore',
          subtitle: 'Last backup: 2 hours ago',
          icon: 'backup-restore',
          type: 'navigation',
          onPress: () => navigation.navigate('Backup'),
        },
        {
          id: 'export',
          title: 'Export Data',
          subtitle: 'Download your data',
          icon: 'download',
          type: 'action',
          onPress: () => Alert.alert('Export Data', 'Data export will be available soon.'),
        },
      ],
    },
    {
      id: 'advanced',
      title: 'Advanced',
      icon: 'cogs',
      items: [
        {
          id: 'analytics',
          title: 'Analytics',
          subtitle: 'Help improve the app',
          icon: 'chart-line',
          type: 'toggle',
          value: settings.analytics,
          onToggle: (value) => handleToggleSetting('analytics', value),
        },
        {
          id: 'crashReporting',
          title: 'Crash Reporting',
          subtitle: 'Send crash reports',
          icon: 'bug',
          type: 'toggle',
          value: settings.crashReporting,
          onToggle: (value) => handleToggleSetting('crashReporting', value),
        },
        {
          id: 'betaFeatures',
          title: 'Beta Features',
          subtitle: 'Try experimental features',
          icon: 'flask',
          type: 'toggle',
          value: settings.betaFeatures,
          onToggle: (value) => handleToggleSetting('betaFeatures', value),
          badge: 'Beta',
        },
        {
          id: 'developer',
          title: 'Developer Options',
          subtitle: 'Debug and development tools',
          icon: 'code-braces',
          type: 'navigation',
          onPress: () => navigation.navigate('Developer'),
          disabled: !settings.betaFeatures,
        },
      ],
    },
    {
      id: 'support',
      title: 'Support',
      icon: 'help-circle',
      items: [
        {
          id: 'help',
          title: 'Help Center',
          subtitle: 'FAQs and guides',
          icon: 'help',
          type: 'navigation',
          onPress: () => navigation.navigate('Help'),
        },
        {
          id: 'contact',
          title: 'Contact Support',
          subtitle: 'Get help from our team',
          icon: 'message',
          type: 'navigation',
          onPress: () => navigation.navigate('Contact'),
        },
        {
          id: 'feedback',
          title: 'Send Feedback',
          subtitle: 'Share your thoughts',
          icon: 'comment',
          type: 'action',
          onPress: () => Alert.alert('Feedback', 'Feedback form will open soon.'),
        },
        {
          id: 'about',
          title: 'About',
          subtitle: 'Version 1.0.0',
          icon: 'information',
          type: 'navigation',
          onPress: () => navigation.navigate('About'),
        },
      ],
    },
    {
      id: 'account-actions',
      title: 'Account Actions',
      icon: 'account-cog',
      items: [
        {
          id: 'signOut',
          title: 'Sign Out',
          subtitle: 'Sign out of your account',
          icon: 'logout',
          type: 'action',
          onPress: handleSignOut,
        },
        {
          id: 'deleteAccount',
          title: 'Delete Account',
          subtitle: 'Permanently delete your account',
          icon: 'delete',
          type: 'action',
          onPress: handleDeleteAccount,
        },
      ],
    },
  ];

  const renderSettingsItem = (item: SettingsItem) => {
    const isDisabled = item.disabled || false;
    
    return (
      <List.Item
        key={item.id}
        title={item.title}
        description={item.subtitle}
        left={(props) => (
          <List.Icon 
            {...props} 
            icon={item.icon} 
            color={isDisabled ? theme.colors.outline : theme.colors.onSurface}
          />
        )}
        right={(props) => {
          if (item.type === 'toggle') {
            return (
              <Switch
                value={item.value as boolean}
                onValueChange={item.onToggle}
                disabled={isDisabled}
              />
            );
          } else if (item.badge) {
            return (
              <View style={styles.rightContainer}>
                <Chip 
                  style={styles.badge}
                  textStyle={styles.badgeText}
                  compact
                >
                  {item.badge}
                </Chip>
                {item.type === 'navigation' && (
                  <Icon name="chevron-right" size={24} color={theme.colors.outline} />
                )}
              </View>
            );
          } else if (item.type === 'navigation') {
            return <List.Icon {...props} icon="chevron-right" />;
          }
          return null;
        }}
        onPress={isDisabled ? undefined : item.onPress}
        disabled={isDisabled}
        style={[styles.listItem, isDisabled && styles.disabledItem]}
        titleStyle={[styles.listItemTitle, isDisabled && styles.disabledText]}
        descriptionStyle={[styles.listItemDescription, isDisabled && styles.disabledText]}
      />
    );
  };

  if (isLoading) {
    return (
      <LoadingSpinner 
        message="Loading settings..."
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <View style={styles.userSection}>
          <Avatar.Text 
            size={64} 
            label={user?.name?.charAt(0) || 'U'}
            style={styles.avatar}
          />
          <View style={styles.userInfo}>
            <Title style={styles.userName}>{user?.name || 'User'}</Title>
            <Paragraph style={styles.userEmail}>{user?.email || 'user@example.com'}</Paragraph>
            <View style={styles.userStats}>
              <Chip style={styles.statChip} compact>
                <Icon name="star" size={12} /> Premium
              </Chip>
              <Chip style={styles.statChip} compact>
                <Icon name="shield-check" size={12} /> Verified
              </Chip>
            </View>
          </View>
          <IconButton
            icon="pencil"
            size={20}
            onPress={() => navigation.navigate('Profile')}
            style={styles.editButton}
          />
        </View>
      </Surface>

      <ScrollView style={styles.content}>
        {settingsSections.map((section) => (
          <Card key={section.id} style={styles.sectionCard}>
            <Card.Content>
              <View style={styles.sectionHeader}>
                <Icon name={section.icon} size={20} color={theme.colors.primary} />
                <Text style={styles.sectionTitle}>{section.title}</Text>
              </View>
              
              {section.items.map((item, index) => (
                <View key={item.id}>
                  {renderSettingsItem(item)}
                  {index < section.items.length - 1 && <Divider style={styles.itemDivider} />}
                </View>
              ))}
            </Card.Content>
          </Card>
        ))}
        
        <View style={styles.footer}>
          <Text style={styles.footerText}>Goliath Quantum Starter v1.0.0</Text>
          <Text style={styles.footerText}>© 2024 Quantum Technologies Inc.</Text>
        </View>
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
  userSection: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  avatar: {
    backgroundColor: theme.colors.primary,
  },
  userInfo: {
    flex: 1,
    marginLeft: 16,
  },
  userName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 8,
  },
  userStats: {
    flexDirection: 'row',
    gap: 8,
  },
  statChip: {
    height: 24,
    backgroundColor: theme.colors.primaryContainer,
  },
  editButton: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  sectionCard: {
    marginBottom: 16,
    elevation: 1,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.outline,
    opacity: 0.3,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginLeft: 8,
  },
  listItem: {
    paddingVertical: 8,
  },
  listItemTitle: {
    fontSize: 16,
    color: theme.colors.onSurface,
  },
  listItemDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  disabledItem: {
    opacity: 0.5,
  },
  disabledText: {
    color: theme.colors.outline,
  },
  rightContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  badge: {
    height: 24,
    backgroundColor: theme.colors.secondaryContainer,
  },
  badgeText: {
    fontSize: 12,
    color: theme.colors.onSecondaryContainer,
  },
  itemDivider: {
    marginVertical: 4,
    opacity: 0.3,
  },
  footer: {
    alignItems: 'center',
    padding: 32,
    marginTop: 16,
  },
  footerText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.5,
    textAlign: 'center',
  },
});

export default SettingsScreen;