import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  Alert,
  Platform,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Switch,
  List,
  Divider,
  Surface,
  Text,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import ReactNativeBiometrics from 'react-native-biometrics';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface BiometricSetupScreenProps {
  navigation: any;
}

const BiometricSetupScreen: React.FC<BiometricSetupScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [biometricEnabled, setBiometricEnabled] = useState(false);
  const [biometricType, setBiometricType] = useState<string>('');
  const [isAvailable, setIsAvailable] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);

  useEffect(() => {
    checkBiometricAvailability();
  }, []);

  const checkBiometricAvailability = async () => {
    try {
      setIsLoading(true);
      const rnBiometrics = new ReactNativeBiometrics();
      
      const { available, biometryType } = await rnBiometrics.isSensorAvailable();
      
      if (available) {
        setIsAvailable(true);
        setBiometricType(biometryType || 'Biometric');
        
        // Check if user has enrolled biometrics
        const { keysExist } = await rnBiometrics.biometricKeysExist();
        setIsEnrolled(keysExist);
      }
    } catch (error) {
      console.error('Biometric check error:', error);
      Alert.alert(
        'Biometric Error',
        'Unable to check biometric availability. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleBiometricToggle = async (enabled: boolean) => {
    if (!isAvailable) {
      Alert.alert(
        'Biometric Not Available',
        'Biometric authentication is not available on this device.'
      );
      return;
    }

    try {
      setIsLoading(true);
      const rnBiometrics = new ReactNativeBiometrics();

      if (enabled) {
        // Enable biometric authentication
        const createKeysResult = await rnBiometrics.createKeys();
        
        if (createKeysResult) {
          // Test biometric authentication
          const authResult = await rnBiometrics.simplePrompt({
            promptMessage: 'Confirm your biometric to enable authentication',
            cancelButtonText: 'Cancel',
          });
          
          if (authResult.success) {
            setBiometricEnabled(true);
            Alert.alert(
              'Success',
              'Biometric authentication has been enabled for your account.'
            );
          } else {
            // Clean up keys if authentication failed
            await rnBiometrics.deleteKeys();
          }
        }
      } else {
        // Disable biometric authentication
        Alert.alert(
          'Disable Biometric',
          'Are you sure you want to disable biometric authentication?',
          [
            {
              text: 'Cancel',
              style: 'cancel',
            },
            {
              text: 'Disable',
              style: 'destructive',
              onPress: async () => {
                await rnBiometrics.deleteKeys();
                setBiometricEnabled(false);
                Alert.alert(
                  'Disabled',
                  'Biometric authentication has been disabled.'
                );
              },
            },
          ]
        );
      }
    } catch (error) {
      console.error('Biometric setup error:', error);
      Alert.alert(
        'Setup Error',
        'Unable to setup biometric authentication. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = () => {
    navigation.navigate('Main');
  };

  const handleContinue = () => {
    navigation.navigate('Main');
  };

  const getBiometricIcon = () => {
    switch (biometricType) {
      case 'FaceID':
        return 'face-recognition';
      case 'TouchID':
      case 'Fingerprint':
        return 'fingerprint';
      default:
        return 'shield-check';
    }
  };

  if (isLoading) {
    return (
      <LoadingSpinner 
        message="Setting up biometric authentication..."
        quantum={true}
      />
    );
  }

  return (
    <View style={styles.container}>
      <Surface style={styles.surface}>
        <View style={styles.header}>
          <Icon 
            name={getBiometricIcon()} 
            size={64} 
            color={theme.colors.primary} 
            style={styles.headerIcon}
          />
          <Title style={styles.title}>Secure Your Account</Title>
          <Paragraph style={styles.subtitle}>
            Enable biometric authentication for quick and secure access to your FLYFOX AI Platform.
          </Paragraph>
        </View>

        <Card style={styles.card}>
          <Card.Content>
            <List.Section>
              <List.Item
                title="Biometric Authentication"
                description={isAvailable ? `Use ${biometricType} to sign in` : 'Not available on this device'}
                left={(props) => (
                  <Icon 
                    {...props} 
                    name={getBiometricIcon()} 
                    size={24} 
                    color={isAvailable ? theme.colors.primary : theme.colors.onSurfaceDisabled}
                  />
                )}
                right={() => (
                  <Switch
                    value={biometricEnabled}
                    onValueChange={handleBiometricToggle}
                    disabled={!isAvailable || isLoading}
                  />
                )}
              />
              
              <Divider />
              
              <List.Item
                title="Device Status"
                description={isAvailable ? 'Biometric sensor detected' : 'No biometric sensor found'}
                left={(props) => (
                  <Icon 
                    {...props} 
                    name={isAvailable ? 'check-circle' : 'alert-circle'} 
                    size={24} 
                    color={isAvailable ? theme.colors.primary : theme.colors.error}
                  />
                )}
              />
              
              {isAvailable && (
                <>
                  <Divider />
                  <List.Item
                    title="Enrollment Status"
                    description={isEnrolled ? 'Biometrics are enrolled' : 'No biometrics enrolled'}
                    left={(props) => (
                      <Icon 
                        {...props} 
                        name={isEnrolled ? 'account-check' : 'account-alert'} 
                        size={24} 
                        color={isEnrolled ? theme.colors.primary : theme.colors.error}
                      />
                    )}
                  />
                </>
              )}
            </List.Section>

            {!isAvailable && (
              <View style={styles.unavailableContainer}>
                <Text style={styles.unavailableText}>
                  Biometric authentication is not available on this device. 
                  You can still use your email and password to sign in securely.
                </Text>
              </View>
            )}

            {isAvailable && !isEnrolled && (
              <View style={styles.warningContainer}>
                <Icon name="information" size={20} color={theme.colors.primary} />
                <Text style={styles.warningText}>
                  Please enroll your biometrics in device settings to use this feature.
                </Text>
              </View>
            )}
          </Card.Content>
        </Card>

        <View style={styles.actions}>
          <Button 
            mode="outlined" 
            onPress={handleSkip}
            style={styles.skipButton}
            disabled={isLoading}
          >
            Skip for Now
          </Button>
          
          <Button 
            mode="contained" 
            onPress={handleContinue}
            style={styles.continueButton}
            disabled={isLoading}
          >
            Continue
          </Button>
        </View>
      </Surface>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    padding: 16,
  },
  surface: {
    flex: 1,
    borderRadius: 16,
    elevation: 4,
    padding: 24,
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  headerIcon: {
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: theme.colors.onSurface,
    opacity: 0.7,
    lineHeight: 24,
  },
  card: {
    marginBottom: 32,
    elevation: 2,
  },
  unavailableContainer: {
    backgroundColor: theme.colors.errorContainer,
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
  },
  unavailableText: {
    color: theme.colors.onErrorContainer,
    fontSize: 14,
    lineHeight: 20,
  },
  warningContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: theme.colors.primaryContainer,
    padding: 16,
    borderRadius: 8,
    marginTop: 16,
  },
  warningText: {
    color: theme.colors.onPrimaryContainer,
    fontSize: 14,
    lineHeight: 20,
    marginLeft: 8,
    flex: 1,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 16,
  },
  skipButton: {
    flex: 1,
  },
  continueButton: {
    flex: 1,
    backgroundColor: theme.colors.primary,
  },
});

export default BiometricSetupScreen;