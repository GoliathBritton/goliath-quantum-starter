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
  Checkbox,
  Text,
  Surface,
  Chip,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { LinearGradient } from 'expo-linear-gradient';

import { RootState, AppDispatch } from '../../store';
import { register } from '../../store/slices/authSlice';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface RegisterScreenProps {
  navigation: any;
}

const RegisterScreen: React.FC<RegisterScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { isLoading } = useSelector((state: RootState) => state.auth);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    role: '',
  });
  
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [selectedTier, setSelectedTier] = useState('STARTER');

  const tiers = [
    {
      id: 'STARTER',
      name: 'Starter',
      credits: 1000,
      features: ['Basic Quantum Operations', '1 Business Pod', 'Email Support'],
    },
    {
      id: 'PROFESSIONAL',
      name: 'Professional',
      credits: 5000,
      features: ['Advanced Quantum Operations', '5 Business Pods', 'Priority Support'],
    },
    {
      id: 'ENTERPRISE',
      name: 'Enterprise',
      credits: 25000,
      features: ['Unlimited Operations', 'Unlimited Pods', '24/7 Support'],
    },
  ];

  const validateEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string) => {
    const minLength = password.length >= 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return {
      isValid: minLength && hasUpper && hasLower && hasNumber && hasSpecial,
      requirements: {
        minLength,
        hasUpper,
        hasLower,
        hasNumber,
        hasSpecial,
      },
    };
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    if (!formData.name.trim()) {
      newErrors.name = 'Full name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }
    
    const passwordValidation = validatePassword(formData.password);
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (!passwordValidation.isValid) {
      newErrors.password = 'Password does not meet requirements';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (!acceptTerms) {
      newErrors.terms = 'You must accept the terms and conditions';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async () => {
    if (!validateForm()) {
      return;
    }
    
    try {
      await dispatch(register({
        ...formData,
        tier: selectedTier,
      })).unwrap();
      
      Alert.alert(
        'Registration Successful',
        'Welcome to the NQBA Platform! Your quantum journey begins now.',
        [{ text: 'OK', onPress: () => navigation.navigate('Login') }]
      );
    } catch (error: any) {
      Alert.alert(
        'Registration Failed',
        error.message || 'Please try again'
      );
    }
  };

  const updateFormData = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const passwordValidation = validatePassword(formData.password);

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
            <Title style={styles.title}>Join NQBA</Title>
            <Paragraph style={styles.subtitle}>
              Start your quantum-enhanced business journey
            </Paragraph>
          </View>

          {/* Registration Form */}
          <Card style={styles.registerCard}>
            <Card.Content>
              <Title style={styles.formTitle}>Create Account</Title>
              
              <TextInput
                label="Full Name"
                value={formData.name}
                onChangeText={(value) => updateFormData('name', value)}
                mode="outlined"
                autoCapitalize="words"
                left={<TextInput.Icon icon="account" />}
                error={!!errors.name}
                style={styles.input}
              />
              {errors.name ? (
                <Text style={styles.errorText}>{errors.name}</Text>
              ) : null}
              
              <TextInput
                label="Email"
                value={formData.email}
                onChangeText={(value) => updateFormData('email', value)}
                mode="outlined"
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
                left={<TextInput.Icon icon="email" />}
                error={!!errors.email}
                style={styles.input}
              />
              {errors.email ? (
                <Text style={styles.errorText}>{errors.email}</Text>
              ) : null}
              
              <TextInput
                label="Company (Optional)"
                value={formData.company}
                onChangeText={(value) => updateFormData('company', value)}
                mode="outlined"
                left={<TextInput.Icon icon="office-building" />}
                style={styles.input}
              />
              
              <TextInput
                label="Role (Optional)"
                value={formData.role}
                onChangeText={(value) => updateFormData('role', value)}
                mode="outlined"
                left={<TextInput.Icon icon="briefcase" />}
                style={styles.input}
              />
              
              <TextInput
                label="Password"
                value={formData.password}
                onChangeText={(value) => updateFormData('password', value)}
                mode="outlined"
                secureTextEntry={!showPassword}
                left={<TextInput.Icon icon="lock" />}
                right={
                  <TextInput.Icon 
                    icon={showPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowPassword(!showPassword)}
                  />
                }
                error={!!errors.password}
                style={styles.input}
              />
              
              {/* Password Requirements */}
              {formData.password && (
                <View style={styles.passwordRequirements}>
                  <Text style={styles.requirementsTitle}>Password Requirements:</Text>
                  <View style={styles.requirementsList}>
                    <View style={styles.requirement}>
                      <Icon 
                        name={passwordValidation.requirements.minLength ? 'check' : 'close'}
                        size={16}
                        color={passwordValidation.requirements.minLength ? theme.colors.primary : theme.colors.error}
                      />
                      <Text style={styles.requirementText}>At least 8 characters</Text>
                    </View>
                    <View style={styles.requirement}>
                      <Icon 
                        name={passwordValidation.requirements.hasUpper ? 'check' : 'close'}
                        size={16}
                        color={passwordValidation.requirements.hasUpper ? theme.colors.primary : theme.colors.error}
                      />
                      <Text style={styles.requirementText}>Uppercase letter</Text>
                    </View>
                    <View style={styles.requirement}>
                      <Icon 
                        name={passwordValidation.requirements.hasLower ? 'check' : 'close'}
                        size={16}
                        color={passwordValidation.requirements.hasLower ? theme.colors.primary : theme.colors.error}
                      />
                      <Text style={styles.requirementText}>Lowercase letter</Text>
                    </View>
                    <View style={styles.requirement}>
                      <Icon 
                        name={passwordValidation.requirements.hasNumber ? 'check' : 'close'}
                        size={16}
                        color={passwordValidation.requirements.hasNumber ? theme.colors.primary : theme.colors.error}
                      />
                      <Text style={styles.requirementText}>Number</Text>
                    </View>
                    <View style={styles.requirement}>
                      <Icon 
                        name={passwordValidation.requirements.hasSpecial ? 'check' : 'close'}
                        size={16}
                        color={passwordValidation.requirements.hasSpecial ? theme.colors.primary : theme.colors.error}
                      />
                      <Text style={styles.requirementText}>Special character</Text>
                    </View>
                  </View>
                </View>
              )}
              
              {errors.password ? (
                <Text style={styles.errorText}>{errors.password}</Text>
              ) : null}
              
              <TextInput
                label="Confirm Password"
                value={formData.confirmPassword}
                onChangeText={(value) => updateFormData('confirmPassword', value)}
                mode="outlined"
                secureTextEntry={!showConfirmPassword}
                left={<TextInput.Icon icon="lock-check" />}
                right={
                  <TextInput.Icon 
                    icon={showConfirmPassword ? 'eye-off' : 'eye'}
                    onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                  />
                }
                error={!!errors.confirmPassword}
                style={styles.input}
              />
              {errors.confirmPassword ? (
                <Text style={styles.errorText}>{errors.confirmPassword}</Text>
              ) : null}
              
              {/* Tier Selection */}
              <View style={styles.tierSection}>
                <Title style={styles.tierTitle}>Choose Your Tier</Title>
                <View style={styles.tierOptions}>
                  {tiers.map((tier) => (
                    <Surface 
                      key={tier.id}
                      style={[
                        styles.tierCard,
                        selectedTier === tier.id && styles.selectedTierCard
                      ]}
                    >
                      <Button
                        mode={selectedTier === tier.id ? 'contained' : 'outlined'}
                        onPress={() => setSelectedTier(tier.id)}
                        style={styles.tierButton}
                      >
                        <View style={styles.tierContent}>
                          <Text style={styles.tierName}>{tier.name}</Text>
                          <Text style={styles.tierCredits}>{tier.credits} credits</Text>
                          <View style={styles.tierFeatures}>
                            {tier.features.map((feature, index) => (
                              <Text key={index} style={styles.tierFeature}>• {feature}</Text>
                            ))}
                          </View>
                        </View>
                      </Button>
                    </Surface>
                  ))}
                </View>
              </View>
              
              {/* Terms and Conditions */}
              <View style={styles.termsContainer}>
                <Checkbox
                  status={acceptTerms ? 'checked' : 'unchecked'}
                  onPress={() => setAcceptTerms(!acceptTerms)}
                />
                <View style={styles.termsText}>
                  <Text>I agree to the </Text>
                  <Button 
                    mode="text" 
                    compact
                    onPress={() => Alert.alert('Info', 'Terms and conditions not implemented yet')}
                  >
                    Terms of Service
                  </Button>
                  <Text> and </Text>
                  <Button 
                    mode="text" 
                    compact
                    onPress={() => Alert.alert('Info', 'Privacy policy not implemented yet')}
                  >
                    Privacy Policy
                  </Button>
                </View>
              </View>
              {errors.terms ? (
                <Text style={styles.errorText}>{errors.terms}</Text>
              ) : null}
              
              <Button
                mode="contained"
                onPress={handleRegister}
                loading={isLoading}
                disabled={isLoading}
                style={styles.registerButton}
                icon="account-plus"
              >
                Create Account
              </Button>
              
              {/* Sign In Link */}
              <View style={styles.signinContainer}>
                <Text style={styles.signinText}>Already have an account? </Text>
                <Button
                  mode="text"
                  onPress={() => navigation.navigate('Login')}
                  compact
                >
                  Sign In
                </Button>
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
  registerCard: {
    marginBottom: 16,
    elevation: 8,
  },
  formTitle: {
    textAlign: 'center',
    marginBottom: 24,
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
  passwordRequirements: {
    marginBottom: 16,
    padding: 12,
    backgroundColor: theme.colors.surfaceVariant,
    borderRadius: 8,
  },
  requirementsTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  requirementsList: {
    gap: 4,
  },
  requirement: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  requirementText: {
    fontSize: 12,
  },
  tierSection: {
    marginVertical: 16,
  },
  tierTitle: {
    fontSize: 18,
    marginBottom: 12,
  },
  tierOptions: {
    gap: 8,
  },
  tierCard: {
    borderRadius: 8,
    elevation: 2,
  },
  selectedTierCard: {
    borderWidth: 2,
    borderColor: theme.colors.primary,
  },
  tierButton: {
    borderRadius: 8,
  },
  tierContent: {
    padding: 8,
  },
  tierName: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  tierCredits: {
    fontSize: 14,
    color: theme.colors.primary,
    marginBottom: 4,
  },
  tierFeatures: {
    gap: 2,
  },
  tierFeature: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
  },
  termsContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginVertical: 16,
  },
  termsText: {
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
    marginLeft: 8,
  },
  registerButton: {
    marginBottom: 16,
    paddingVertical: 4,
  },
  signinContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  signinText: {
    color: theme.colors.onSurfaceVariant,
  },
});

export default RegisterScreen;