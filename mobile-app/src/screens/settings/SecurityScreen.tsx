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
  TextInput,
  IconButton,
  Chip,
  ProgressBar,
  Dialog,
  Portal,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface SecurityScreenProps {
  navigation: any;
}

interface SecuritySetting {
  id: string;
  title: string;
  subtitle: string;
  icon: string;
  type: 'toggle' | 'action' | 'info';
  value?: boolean;
  status?: 'enabled' | 'disabled' | 'pending' | 'error';
  onPress?: () => void;
  onToggle?: (value: boolean) => void;
  badge?: string;
  critical?: boolean;
}

interface LoginSession {
  id: string;
  device: string;
  location: string;
  ipAddress: string;
  lastActive: string;
  current: boolean;
  browser?: string;
  os?: string;
}

const SecurityScreen: React.FC<SecurityScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [showPasswordDialog, setShowPasswordDialog] = useState(false);
  const [showTwoFactorDialog, setShowTwoFactorDialog] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [twoFactorCode, setTwoFactorCode] = useState('');
  
  const [securitySettings, setSecuritySettings] = useState({
    biometricAuth: false,
    twoFactorAuth: false,
    loginNotifications: true,
    deviceTracking: true,
    sessionTimeout: true,
    quantumEncryption: true,
    autoLock: true,
    remoteWipe: false,
  });
  
  const [loginSessions, setLoginSessions] = useState<LoginSession[]>([]);
  const [passwordStrength, setPasswordStrength] = useState({
    score: 3,
    feedback: ['Use a longer password', 'Add special characters'],
  });

  useEffect(() => {
    loadSecurityData();
  }, []);

  const loadSecurityData = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock login sessions data
      const mockSessions: LoginSession[] = [
        {
          id: '1',
          device: 'iPhone 15 Pro',
          location: 'New York, NY',
          ipAddress: '192.168.1.100',
          lastActive: new Date().toISOString(),
          current: true,
          browser: 'Safari',
          os: 'iOS 17.2',
        },
        {
          id: '2',
          device: 'MacBook Pro',
          location: 'New York, NY',
          ipAddress: '192.168.1.101',
          lastActive: new Date(Date.now() - 3600000).toISOString(),
          current: false,
          browser: 'Chrome',
          os: 'macOS 14.2',
        },
        {
          id: '3',
          device: 'Windows PC',
          location: 'San Francisco, CA',
          ipAddress: '10.0.0.50',
          lastActive: new Date(Date.now() - 86400000).toISOString(),
          current: false,
          browser: 'Edge',
          os: 'Windows 11',
        },
      ];
      
      setLoginSessions(mockSessions);
      
    } catch (error) {
      console.error('Load security data error:', error);
      Alert.alert('Error', 'Failed to load security data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleSetting = (key: string, value: boolean) => {
    if (key === 'twoFactorAuth' && value) {
      setShowTwoFactorDialog(true);
      return;
    }
    
    setSecuritySettings(prev => ({ ...prev, [key]: value }));
    saveSetting(key, value);
  };

  const saveSetting = async (key: string, value: any) => {
    try {
      console.log(`Saving security setting ${key}:`, value);
      // Save to API
    } catch (error) {
      console.error('Save setting error:', error);
      Alert.alert('Error', 'Failed to save setting');
    }
  };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }
    
    if (newPassword.length < 8) {
      Alert.alert('Error', 'Password must be at least 8 characters long');
      return;
    }
    
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      Alert.alert('Success', 'Password changed successfully');
      setShowPasswordDialog(false);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      
    } catch (error) {
      console.error('Change password error:', error);
      Alert.alert('Error', 'Failed to change password');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnable2FA = async () => {
    if (twoFactorCode.length !== 6) {
      Alert.alert('Error', 'Please enter a valid 6-digit code');
      return;
    }
    
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSecuritySettings(prev => ({ ...prev, twoFactorAuth: true }));
      Alert.alert('Success', 'Two-factor authentication enabled');
      setShowTwoFactorDialog(false);
      setTwoFactorCode('');
      
    } catch (error) {
      console.error('Enable 2FA error:', error);
      Alert.alert('Error', 'Failed to enable two-factor authentication');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTerminateSession = (sessionId: string) => {
    Alert.alert(
      'Terminate Session',
      'Are you sure you want to terminate this session?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Terminate',
          style: 'destructive',
          onPress: async () => {
            try {
              // Simulate API call
              await new Promise(resolve => setTimeout(resolve, 500));
              setLoginSessions(prev => prev.filter(session => session.id !== sessionId));
              Alert.alert('Success', 'Session terminated');
            } catch (error) {
              Alert.alert('Error', 'Failed to terminate session');
            }
          },
        },
      ]
    );
  };

  const handleTerminateAllSessions = () => {
    Alert.alert(
      'Terminate All Sessions',
      'This will sign you out of all devices except this one.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Terminate All',
          style: 'destructive',
          onPress: async () => {
            try {
              // Simulate API call
              await new Promise(resolve => setTimeout(resolve, 1000));
              setLoginSessions(prev => prev.filter(session => session.current));
              Alert.alert('Success', 'All other sessions terminated');
            } catch (error) {
              Alert.alert('Error', 'Failed to terminate sessions');
            }
          },
        },
      ]
    );
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'enabled':
        return theme.colors.primary;
      case 'disabled':
        return theme.colors.outline;
      case 'pending':
        return theme.colors.tertiary;
      case 'error':
        return theme.colors.error;
      default:
        return theme.colors.outline;
    }
  };

  const getPasswordStrengthColor = (score: number) => {
    if (score <= 1) return theme.colors.error;
    if (score <= 2) return '#FF9800';
    if (score <= 3) return '#FFC107';
    return theme.colors.primary;
  };

  const getPasswordStrengthText = (score: number) => {
    if (score <= 1) return 'Weak';
    if (score <= 2) return 'Fair';
    if (score <= 3) return 'Good';
    return 'Strong';
  };

  const securitySections = [
    {
      title: 'Authentication',
      items: [
        {
          id: 'password',
          title: 'Change Password',
          subtitle: 'Update your account password',
          icon: 'key',
          type: 'action' as const,
          onPress: () => setShowPasswordDialog(true),
        },
        {
          id: 'biometricAuth',
          title: 'Biometric Authentication',
          subtitle: 'Use fingerprint or face recognition',
          icon: 'fingerprint',
          type: 'toggle' as const,
          value: securitySettings.biometricAuth,
          onToggle: (value) => handleToggleSetting('biometricAuth', value),
          status: securitySettings.biometricAuth ? 'enabled' : 'disabled',
        },
        {
          id: 'twoFactorAuth',
          title: 'Two-Factor Authentication',
          subtitle: 'Add an extra layer of security',
          icon: 'two-factor-authentication',
          type: 'toggle' as const,
          value: securitySettings.twoFactorAuth,
          onToggle: (value) => handleToggleSetting('twoFactorAuth', value),
          status: securitySettings.twoFactorAuth ? 'enabled' : 'disabled',
          critical: true,
        },
      ],
    },
    {
      title: 'Privacy & Monitoring',
      items: [
        {
          id: 'loginNotifications',
          title: 'Login Notifications',
          subtitle: 'Get notified of new sign-ins',
          icon: 'bell-alert',
          type: 'toggle' as const,
          value: securitySettings.loginNotifications,
          onToggle: (value) => handleToggleSetting('loginNotifications', value),
        },
        {
          id: 'deviceTracking',
          title: 'Device Tracking',
          subtitle: 'Monitor device access',
          icon: 'devices',
          type: 'toggle' as const,
          value: securitySettings.deviceTracking,
          onToggle: (value) => handleToggleSetting('deviceTracking', value),
        },
        {
          id: 'sessionTimeout',
          title: 'Session Timeout',
          subtitle: 'Auto-logout after inactivity',
          icon: 'timer',
          type: 'toggle' as const,
          value: securitySettings.sessionTimeout,
          onToggle: (value) => handleToggleSetting('sessionTimeout', value),
        },
      ],
    },
    {
      title: 'Advanced Security',
      items: [
        {
          id: 'quantumEncryption',
          title: 'Quantum Encryption',
          subtitle: 'Enhanced quantum-safe encryption',
          icon: 'shield-lock',
          type: 'toggle' as const,
          value: securitySettings.quantumEncryption,
          onToggle: (value) => handleToggleSetting('quantumEncryption', value),
          badge: 'Beta',
        },
        {
          id: 'autoLock',
          title: 'Auto Lock',
          subtitle: 'Lock app when backgrounded',
          icon: 'lock',
          type: 'toggle' as const,
          value: securitySettings.autoLock,
          onToggle: (value) => handleToggleSetting('autoLock', value),
        },
        {
          id: 'remoteWipe',
          title: 'Remote Wipe',
          subtitle: 'Enable remote data deletion',
          icon: 'delete-sweep',
          type: 'toggle' as const,
          value: securitySettings.remoteWipe,
          onToggle: (value) => handleToggleSetting('remoteWipe', value),
          critical: true,
        },
      ],
    },
  ];

  if (isLoading && loginSessions.length === 0) {
    return (
      <LoadingSpinner 
        message="Loading security settings..."
      />
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.content}>
        {/* Security Overview */}
        <Card style={styles.overviewCard}>
          <Card.Content>
            <Title style={styles.overviewTitle}>Security Overview</Title>
            <View style={styles.securityScore}>
              <View style={styles.scoreCircle}>
                <Text style={styles.scoreText}>85%</Text>
              </View>
              <View style={styles.scoreInfo}>
                <Text style={styles.scoreLabel}>Security Score</Text>
                <Text style={styles.scoreDescription}>
                  Your account is well protected. Consider enabling 2FA for better security.
                </Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Security Settings */}
        {securitySections.map((section) => (
          <Card key={section.title} style={styles.sectionCard}>
            <Card.Content>
              <Text style={styles.sectionTitle}>{section.title}</Text>
              
              {section.items.map((item, index) => (
                <View key={item.id}>
                  <List.Item
                    title={item.title}
                    description={item.subtitle}
                    left={(props) => (
                      <View style={styles.leftContainer}>
                        <List.Icon 
                          {...props} 
                          icon={item.icon} 
                          color={item.critical ? theme.colors.error : theme.colors.onSurface}
                        />
                        {item.critical && (
                          <Icon 
                            name="alert" 
                            size={12} 
                            color={theme.colors.error} 
                            style={styles.criticalIcon}
                          />
                        )}
                      </View>
                    )}
                    right={(props) => {
                      if (item.type === 'toggle') {
                        return (
                          <View style={styles.rightContainer}>
                            {item.badge && (
                              <Chip 
                                style={styles.badge}
                                textStyle={styles.badgeText}
                                compact
                              >
                                {item.badge}
                              </Chip>
                            )}
                            <Switch
                              value={item.value as boolean}
                              onValueChange={item.onToggle}
                            />
                          </View>
                        );
                      } else if (item.type === 'action') {
                        return <List.Icon {...props} icon="chevron-right" />;
                      }
                      return null;
                    }}
                    onPress={item.onPress}
                    style={styles.listItem}
                  />
                  {index < section.items.length - 1 && <Divider style={styles.itemDivider} />}
                </View>
              ))}
            </Card.Content>
          </Card>
        ))}

        {/* Active Sessions */}
        <Card style={styles.sectionCard}>
          <Card.Content>
            <View style={styles.sessionsHeader}>
              <Text style={styles.sectionTitle}>Active Sessions</Text>
              <Button 
                mode="outlined" 
                compact 
                onPress={handleTerminateAllSessions}
                style={styles.terminateAllButton}
              >
                Terminate All
              </Button>
            </View>
            
            {loginSessions.map((session, index) => (
              <View key={session.id}>
                <View style={styles.sessionItem}>
                  <View style={styles.sessionIcon}>
                    <Icon 
                      name={session.device.includes('iPhone') || session.device.includes('Android') ? 'cellphone' : 'laptop'} 
                      size={24} 
                      color={session.current ? theme.colors.primary : theme.colors.onSurface}
                    />
                    {session.current && (
                      <View style={styles.currentBadge}>
                        <Icon name="check" size={12} color={theme.colors.onPrimary} />
                      </View>
                    )}
                  </View>
                  
                  <View style={styles.sessionInfo}>
                    <View style={styles.sessionHeader}>
                      <Text style={styles.sessionDevice}>{session.device}</Text>
                      {session.current && (
                        <Chip style={styles.currentChip} compact>
                          Current
                        </Chip>
                      )}
                    </View>
                    <Text style={styles.sessionLocation}>
                      {session.location} • {session.browser} on {session.os}
                    </Text>
                    <Text style={styles.sessionTime}>
                      Last active: {new Date(session.lastActive).toLocaleString()}
                    </Text>
                    <Text style={styles.sessionIP}>IP: {session.ipAddress}</Text>
                  </View>
                  
                  {!session.current && (
                    <IconButton
                      icon="close"
                      size={20}
                      onPress={() => handleTerminateSession(session.id)}
                      style={styles.terminateButton}
                    />
                  )}
                </View>
                {index < loginSessions.length - 1 && <Divider style={styles.sessionDivider} />}
              </View>
            ))}
          </Card.Content>
        </Card>
      </ScrollView>

      {/* Change Password Dialog */}
      <Portal>
        <Dialog visible={showPasswordDialog} onDismiss={() => setShowPasswordDialog(false)}>
          <Dialog.Title>Change Password</Dialog.Title>
          <Dialog.Content>
            <TextInput
              label="Current Password"
              value={currentPassword}
              onChangeText={setCurrentPassword}
              secureTextEntry
              style={styles.passwordInput}
              mode="outlined"
            />
            <TextInput
              label="New Password"
              value={newPassword}
              onChangeText={setNewPassword}
              secureTextEntry
              style={styles.passwordInput}
              mode="outlined"
            />
            <TextInput
              label="Confirm New Password"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              secureTextEntry
              style={styles.passwordInput}
              mode="outlined"
            />
            
            {newPassword.length > 0 && (
              <View style={styles.passwordStrength}>
                <Text style={styles.strengthLabel}>Password Strength</Text>
                <ProgressBar 
                  progress={passwordStrength.score / 4} 
                  color={getPasswordStrengthColor(passwordStrength.score)}
                  style={styles.strengthBar}
                />
                <Text style={[styles.strengthText, { color: getPasswordStrengthColor(passwordStrength.score) }]}>
                  {getPasswordStrengthText(passwordStrength.score)}
                </Text>
              </View>
            )}
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setShowPasswordDialog(false)}>Cancel</Button>
            <Button 
              mode="contained" 
              onPress={handleChangePassword}
              disabled={!currentPassword || !newPassword || !confirmPassword}
            >
              Change Password
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>

      {/* Two-Factor Authentication Dialog */}
      <Portal>
        <Dialog visible={showTwoFactorDialog} onDismiss={() => setShowTwoFactorDialog(false)}>
          <Dialog.Title>Enable Two-Factor Authentication</Dialog.Title>
          <Dialog.Content>
            <Paragraph style={styles.twoFactorDescription}>
              Scan the QR code with your authenticator app and enter the 6-digit code.
            </Paragraph>
            
            <View style={styles.qrCodePlaceholder}>
              <Icon name="qrcode" size={120} color={theme.colors.outline} />
              <Text style={styles.qrCodeText}>QR Code</Text>
            </View>
            
            <TextInput
              label="6-digit code"
              value={twoFactorCode}
              onChangeText={setTwoFactorCode}
              keyboardType="numeric"
              maxLength={6}
              style={styles.twoFactorInput}
              mode="outlined"
            />
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setShowTwoFactorDialog(false)}>Cancel</Button>
            <Button 
              mode="contained" 
              onPress={handleEnable2FA}
              disabled={twoFactorCode.length !== 6}
            >
              Enable 2FA
            </Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  overviewCard: {
    marginBottom: 16,
    elevation: 2,
  },
  overviewTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 16,
  },
  securityScore: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  scoreCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: theme.colors.primaryContainer,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  scoreText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.onPrimaryContainer,
  },
  scoreInfo: {
    flex: 1,
  },
  scoreLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  scoreDescription: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 20,
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
  listItem: {
    paddingVertical: 8,
  },
  leftContainer: {
    position: 'relative',
  },
  criticalIcon: {
    position: 'absolute',
    top: 0,
    right: 0,
    backgroundColor: theme.colors.surface,
    borderRadius: 6,
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
  sessionsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  terminateAllButton: {
    borderColor: theme.colors.error,
  },
  sessionItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    paddingVertical: 12,
  },
  sessionIcon: {
    position: 'relative',
    marginRight: 12,
  },
  currentBadge: {
    position: 'absolute',
    top: -4,
    right: -4,
    width: 16,
    height: 16,
    borderRadius: 8,
    backgroundColor: theme.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sessionInfo: {
    flex: 1,
  },
  sessionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  sessionDevice: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginRight: 8,
  },
  currentChip: {
    height: 20,
    backgroundColor: theme.colors.primaryContainer,
  },
  sessionLocation: {
    fontSize: 14,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 2,
  },
  sessionTime: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginBottom: 2,
  },
  sessionIP: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.5,
    fontFamily: 'monospace',
  },
  terminateButton: {
    backgroundColor: theme.colors.errorContainer,
  },
  sessionDivider: {
    marginVertical: 8,
    opacity: 0.3,
  },
  passwordInput: {
    marginBottom: 12,
  },
  passwordStrength: {
    marginTop: 8,
  },
  strengthLabel: {
    fontSize: 14,
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  strengthBar: {
    height: 6,
    borderRadius: 3,
    marginBottom: 4,
  },
  strengthText: {
    fontSize: 12,
    fontWeight: '600',
  },
  twoFactorDescription: {
    marginBottom: 16,
    textAlign: 'center',
  },
  qrCodePlaceholder: {
    alignItems: 'center',
    padding: 24,
    backgroundColor: theme.colors.surfaceVariant,
    borderRadius: 8,
    marginBottom: 16,
  },
  qrCodeText: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    marginTop: 8,
  },
  twoFactorInput: {
    textAlign: 'center',
    fontSize: 18,
    letterSpacing: 4,
  },
});

export default SecurityScreen;