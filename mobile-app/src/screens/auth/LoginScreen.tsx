import React, { useState } from 'react';
import {
  View,
  ScrollView,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  TextInput,
  Button,
  Divider,
  Text,
  Surface,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { LinearGradient } from 'expo-linear-gradient';

import { RootState, AppDispatch } from '../../store';
import { login } from '../../store/slices/authSlice';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface LoginScreenProps {
  navigation: any;
}

const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { isLoading, error } = useSelector((state: RootState) => state.auth);
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validateForm = () => {
    let isValid = true;
    
    if (!email) {
      setEmailError('Email is required');
      isValid = false;
    } else if (!validateEmail(email)) {
      setEmailError('Please enter a valid email');
      isValid = false;
    } else {
      setEmailError('');
    }
    
    if (!password) {
      setPasswordError('Password is required');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      isValid = false;
    } else {
      setPasswordError('');
    }
    
    return isValid;
  };

  const handleLogin = async () => {
    if (!validateForm()) {
      return;
    }
    
    try {
      await dispatch(login({ email, password })).unwrap();
      // Navigation will be handled by the auth state change
    } catch (error: any) {
      Alert.alert(
        'Login Failed',
        error.message || 'Please check your credentials and try again'
      );
    }
  };

  const handleSocialLogin = (provider: string) => {
    Alert.alert('Info', `${provider} login not implemented yet`);
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <LinearGradient
        colors={[theme.colors.primary, theme.colors.secondary]}
        style={styles.gradient}
      >
        <ScrollView 
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          {/* Header */}
          <View style={styles.header}>
            <Surface style={styles.logoContainer}>
              <Icon name="atom" size={48} color={theme.colors.primary} />
            </Surface>
            <Title style={styles.title}>NQBA Platform</Title>
            <Paragraph style={styles.subtitle}>
              Quantum-Enhanced Business Intelligence
            </Paragraph>
          </View>

          {/* Login Form */}
          <Card style={styles.loginCard}>
            <Card.Content>
              <Title style={styles.formTitle}>Welcome Back</Title>
              <Paragraph style={styles.formSubtitle}>
                Sign in to access your quantum-powered dashboard
              </Paragraph>
              
              <TextInput
                label="Email"
                value={email}
                onChangeText={setEmail}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                left={<TextInput.Icon icon="email" />}
                error={!!emailError}
                style={styles.input}
              />
              {emailError ? (
                <Text style={styles.errorText}>{emailError}</Text>
              ) : null}
              
              <TextInput
                label="Password"
                value={password}
                onChangeText={setPassword}
                mode="outlined"
                secureTextEntry={!showPassword}
                autoComplete="password"
                left={<TextInput.Icon icon="lock" />}
                right={
                  <TextInput.Icon 
                    icon={showPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowPassword(!showPassword)}
                  />
                }
                error={!!passwordError}
                style={styles.input}
              />
              {passwordError ? (
                <Text style={styles.errorText}>{passwordError}</Text>
              ) : null}
              
              <Button
                mode="text"
                onPress={() => Alert.alert('Info', 'Password reset not implemented yet')}
                style={styles.forgotButton}
              >
                Forgot Password?
              </Button>
              
              <Button
                mode="contained"
                onPress={handleLogin}
                loading={isLoading}
                disabled={isLoading}
                style={styles.loginButton}
                icon="login"
              >
                Sign In
              </Button>
              
              <Divider style={styles.divider} />
              
              {/* Social Login */}
              <View style={styles.socialContainer}>
                <Text style={styles.socialText}>Or continue with</Text>
                <View style={styles.socialButtons}>
                  <Button
                    mode="outlined"
                    onPress={() => handleSocialLogin('Google')}
                    style={styles.socialButton}
                    icon="google"
                  >
                    Google
                  </Button>
                  <Button
                    mode="outlined"
                    onPress={() => handleSocialLogin('Apple')}
                    style={styles.socialButton}
                    icon="apple"
                  >
                    Apple
                  </Button>
                </View>
              </View>
              
              {/* Sign Up Link */}
              <View style={styles.signupContainer}>
                <Text style={styles.signupText}>Don't have an account? </Text>
                <Button
                  mode="text"
                  onPress={() => navigation.navigate('Register')}
                  compact
                >
                  Sign Up
                </Button>
              </View>
            </Card.Content>
          </Card>
          
          {/* Features Preview */}
          <Card style={styles.featuresCard}>
            <Card.Content>
              <Title style={styles.featuresTitle}>Quantum Advantage</Title>
              <View style={styles.featuresList}>
                <View style={styles.featureItem}>
                  <Icon name="atom" size={20} color={theme.colors.primary} />
                  <Text style={styles.featureText}>410.7x Quantum Speed-up</Text>
                </View>
                <View style={styles.featureItem}>
                  <Icon name="shield-check" size={20} color={theme.colors.primary} />
                  <Text style={styles.featureText}>Enterprise Security</Text>
                </View>
                <View style={styles.featureItem}>
                  <Icon name="brain" size={20} color={theme.colors.primary} />
                  <Text style={styles.featureText}>AI-Powered Insights</Text>
                </View>
                <View style={styles.featureItem}>
                  <Icon name="chart-line" size={20} color={theme.colors.primary} />
                  <Text style={styles.featureText}>Real-time Analytics</Text>
                </View>
              </View>
            </Card.Content>
          </Card>
        </ScrollView>
      </LinearGradient>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    padding: 16,
  },
  header: {
    alignItems: 'center',
    marginTop: 40,
    marginBottom: 32,
  },
  logoContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
    elevation: 4,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
  },
  loginCard: {
    marginBottom: 16,
    elevation: 8,
  },
  formTitle: {
    textAlign: 'center',
    marginBottom: 8,
  },
  formSubtitle: {
    textAlign: 'center',
    marginBottom: 24,
    color: theme.colors.onSurfaceVariant,
  },
  input: {
    marginBottom: 8,
  },
  errorText: {
    color: theme.colors.error,
    fontSize: 12,
    marginBottom: 8,
    marginLeft: 12,
  },
  forgotButton: {
    alignSelf: 'flex-end',
    marginBottom: 16,
  },
  loginButton: {
    marginBottom: 24,
    paddingVertical: 4,
  },
  divider: {
    marginBottom: 24,
  },
  socialContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },
  socialText: {
    marginBottom: 16,
    color: theme.colors.onSurfaceVariant,
  },
  socialButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  socialButton: {
    flex: 1,
  },
  signupContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  signupText: {
    color: theme.colors.onSurfaceVariant,
  },
  featuresCard: {
    elevation: 4,
  },
  featuresTitle: {
    textAlign: 'center',
    marginBottom: 16,
  },
  featuresList: {
    gap: 12,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  featureText: {
    fontSize: 14,
    color: theme.colors.onSurface,
  },
});

export default LoginScreen;