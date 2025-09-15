import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  Image,
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
  Switch,
  TextInput,
  Menu,
  IconButton,
} from 'react-native-paper';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState, AppDispatch } from '../../store';
import { theme } from '../../theme';
import LoadingSpinner from '../../components/LoadingSpinner';

interface ProfileScreenProps {
  navigation: any;
}

interface UserProfile {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  avatar?: string;
  role: string;
  department: string;
  joinDate: string;
  lastLogin: string;
  preferences: {
    notifications: boolean;
    darkMode: boolean;
    biometric: boolean;
    analytics: boolean;
  };
  stats: {
    operationsRun: number;
    circuitsCreated: number;
    algorithmsUsed: number;
    computeHours: number;
  };
}

const ProfileScreen: React.FC<ProfileScreenProps> = ({ navigation }) => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [isLoading, setIsLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [menuVisible, setMenuVisible] = useState(false);
  const [profile, setProfile] = useState<UserProfile>({
    id: user?.id || '1',
    email: user?.email || 'user@flyfox.ai',
    firstName: user?.firstName || 'John',
    lastName: user?.lastName || 'Doe',
    avatar: user?.avatar,
    role: 'Quantum Developer',
    department: 'Research & Development',
    joinDate: '2024-01-15',
    lastLogin: new Date().toISOString(),
    preferences: {
      notifications: true,
      darkMode: false,
      biometric: true,
      analytics: true,
    },
    stats: {
      operationsRun: 127,
      circuitsCreated: 45,
      algorithmsUsed: 12,
      computeHours: 89.5,
    },
  });
  const [editedProfile, setEditedProfile] = useState(profile);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Profile data would be loaded from API
    } catch (error) {
      console.error('Load profile error:', error);
      Alert.alert('Error', 'Failed to load profile data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveProfile = async () => {
    try {
      setIsLoading(true);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setProfile(editedProfile);
      setIsEditing(false);
      
      Alert.alert('Success', 'Profile updated successfully');
    } catch (error) {
      console.error('Save profile error:', error);
      Alert.alert('Error', 'Failed to update profile');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setEditedProfile(profile);
    setIsEditing(false);
  };

  const handlePreferenceChange = (key: keyof UserProfile['preferences'], value: boolean) => {
    setEditedProfile(prev => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [key]: value,
      },
    }));
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: () => {
            // Dispatch logout action
            navigation.navigate('Auth');
          },
        },
      ]
    );
  };

  const handleChangePassword = () => {
    navigation.navigate('ChangePassword');
  };

  const handleBiometricSettings = () => {
    navigation.navigate('BiometricSetup');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatLastLogin = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (diffHours < 1) {
      return 'Just now';
    } else if (diffHours < 24) {
      return `${diffHours} hours ago`;
    } else {
      return formatDate(dateString);
    }
  };

  if (isLoading && !profile.id) {
    return (
      <LoadingSpinner 
        message="Loading profile..."
        quantum={true}
      />
    );
  }

  const currentProfile = isEditing ? editedProfile : profile;

  return (
    <View style={styles.container}>
      <Surface style={styles.header}>
        <View style={styles.headerContent}>
          <View style={styles.avatarContainer}>
            {currentProfile.avatar ? (
              <Image source={{ uri: currentProfile.avatar }} style={styles.avatar} />
            ) : (
              <Avatar.Text 
                size={80} 
                label={`${currentProfile.firstName[0]}${currentProfile.lastName[0]}`}
                style={styles.avatarText}
              />
            )}
            {isEditing && (
              <IconButton
                icon="camera"
                size={20}
                style={styles.cameraButton}
                onPress={() => Alert.alert('Info', 'Avatar upload coming soon')}
              />
            )}
          </View>
          
          <View style={styles.userInfo}>
            {isEditing ? (
              <View style={styles.editContainer}>
                <TextInput
                  value={editedProfile.firstName}
                  onChangeText={(text) => setEditedProfile(prev => ({ ...prev, firstName: text }))}
                  style={styles.editInput}
                  mode="outlined"
                  label="First Name"
                  dense
                />
                <TextInput
                  value={editedProfile.lastName}
                  onChangeText={(text) => setEditedProfile(prev => ({ ...prev, lastName: text }))}
                  style={styles.editInput}
                  mode="outlined"
                  label="Last Name"
                  dense
                />
              </View>
            ) : (
              <>
                <Title style={styles.userName}>
                  {currentProfile.firstName} {currentProfile.lastName}
                </Title>
                <Paragraph style={styles.userRole}>{currentProfile.role}</Paragraph>
                <Paragraph style={styles.userDepartment}>{currentProfile.department}</Paragraph>
              </>
            )}
          </View>
          
          <Menu
            visible={menuVisible}
            onDismiss={() => setMenuVisible(false)}
            anchor={
              <IconButton
                icon="dots-vertical"
                onPress={() => setMenuVisible(true)}
              />
            }
          >
            <Menu.Item
              onPress={() => {
                setMenuVisible(false);
                setIsEditing(!isEditing);
              }}
              title={isEditing ? 'Cancel Edit' : 'Edit Profile'}
              leadingIcon={isEditing ? 'close' : 'pencil'}
            />
            <Menu.Item
              onPress={() => {
                setMenuVisible(false);
                handleChangePassword();
              }}
              title="Change Password"
              leadingIcon="lock"
            />
            <Divider />
            <Menu.Item
              onPress={() => {
                setMenuVisible(false);
                handleLogout();
              }}
              title="Logout"
              leadingIcon="logout"
            />
          </Menu>
        </View>
      </Surface>

      <ScrollView style={styles.content}>
        {/* Account Information */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.sectionTitle}>Account Information</Title>
            <List.Item
              title="Email"
              description={currentProfile.email}
              left={(props) => <Icon {...props} name="email" size={24} />}
            />
            <List.Item
              title="Member Since"
              description={formatDate(currentProfile.joinDate)}
              left={(props) => <Icon {...props} name="calendar" size={24} />}
            />
            <List.Item
              title="Last Login"
              description={formatLastLogin(currentProfile.lastLogin)}
              left={(props) => <Icon {...props} name="clock" size={24} />}
            />
          </Card.Content>
        </Card>

        {/* Statistics */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.sectionTitle}>Usage Statistics</Title>
            <View style={styles.statsGrid}>
              <View style={styles.statItem}>
                <Icon name="play-circle" size={32} color={theme.colors.primary} />
                <Text style={styles.statNumber}>{currentProfile.stats.operationsRun}</Text>
                <Text style={styles.statLabel}>Operations Run</Text>
              </View>
              <View style={styles.statItem}>
                <Icon name="resistor-nodes" size={32} color={theme.colors.secondary} />
                <Text style={styles.statNumber}>{currentProfile.stats.circuitsCreated}</Text>
                <Text style={styles.statLabel}>Circuits Created</Text>
              </View>
              <View style={styles.statItem}>
                <Icon name="function-variant" size={32} color={theme.colors.tertiary} />
                <Text style={styles.statNumber}>{currentProfile.stats.algorithmsUsed}</Text>
                <Text style={styles.statLabel}>Algorithms Used</Text>
              </View>
              <View style={styles.statItem}>
                <Icon name="timer" size={32} color={theme.colors.primary} />
                <Text style={styles.statNumber}>{currentProfile.stats.computeHours}</Text>
                <Text style={styles.statLabel}>Compute Hours</Text>
              </View>
            </View>
          </Card.Content>
        </Card>

        {/* Preferences */}
        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.sectionTitle}>Preferences</Title>
            <List.Item
              title="Push Notifications"
              description="Receive notifications about operations and updates"
              left={(props) => <Icon {...props} name="bell" size={24} />}
              right={() => (
                <Switch
                  value={currentProfile.preferences.notifications}
                  onValueChange={(value) => handlePreferenceChange('notifications', value)}
                  disabled={!isEditing}
                />
              )}
            />
            <List.Item
              title="Dark Mode"
              description="Use dark theme for the application"
              left={(props) => <Icon {...props} name="theme-light-dark" size={24} />}
              right={() => (
                <Switch
                  value={currentProfile.preferences.darkMode}
                  onValueChange={(value) => handlePreferenceChange('darkMode', value)}
                  disabled={!isEditing}
                />
              )}
            />
            <List.Item
              title="Biometric Authentication"
              description="Use fingerprint or face recognition"
              left={(props) => <Icon {...props} name="fingerprint" size={24} />}
              right={() => (
                <Switch
                  value={currentProfile.preferences.biometric}
                  onValueChange={(value) => handlePreferenceChange('biometric', value)}
                  disabled={!isEditing}
                />
              )}
              onPress={handleBiometricSettings}
            />
            <List.Item
              title="Usage Analytics"
              description="Help improve the app by sharing usage data"
              left={(props) => <Icon {...props} name="chart-line" size={24} />}
              right={() => (
                <Switch
                  value={currentProfile.preferences.analytics}
                  onValueChange={(value) => handlePreferenceChange('analytics', value)}
                  disabled={!isEditing}
                />
              )}
            />
          </Card.Content>
        </Card>

        {isEditing && (
          <View style={styles.editActions}>
            <Button 
              mode="outlined" 
              onPress={handleCancelEdit}
              style={styles.cancelButton}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button 
              mode="contained" 
              onPress={handleSaveProfile}
              style={styles.saveButton}
              loading={isLoading}
              disabled={isLoading}
            >
              Save Changes
            </Button>
          </View>
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
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
  },
  avatarContainer: {
    position: 'relative',
    marginRight: 16,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
  },
  avatarText: {
    backgroundColor: theme.colors.primary,
  },
  cameraButton: {
    position: 'absolute',
    bottom: -5,
    right: -5,
    backgroundColor: theme.colors.primary,
  },
  userInfo: {
    flex: 1,
  },
  userName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginBottom: 4,
  },
  userRole: {
    fontSize: 14,
    color: theme.colors.primary,
    fontWeight: '600',
  },
  userDepartment: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
  },
  editContainer: {
    gap: 8,
  },
  editInput: {
    height: 40,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: theme.colors.onSurface,
    marginBottom: 8,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statItem: {
    width: '48%',
    alignItems: 'center',
    padding: 16,
    backgroundColor: theme.colors.surfaceVariant,
    borderRadius: 12,
    marginBottom: 8,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: theme.colors.onSurface,
    opacity: 0.7,
    textAlign: 'center',
    marginTop: 4,
  },
  editActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 16,
    marginTop: 16,
    marginBottom: 32,
  },
  cancelButton: {
    flex: 1,
  },
  saveButton: {
    flex: 1,
    backgroundColor: theme.colors.primary,
  },
});

export default ProfileScreen;