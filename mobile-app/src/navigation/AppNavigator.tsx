import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import { RootState } from '../store';
import { theme } from '../theme';

// Auth Screens
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import BiometricSetupScreen from '../screens/auth/BiometricSetupScreen';

// Main Screens
import DashboardScreen from '../screens/main/DashboardScreen';
import BusinessPodsScreen from '../screens/main/BusinessPodsScreen';
import QuantumOperationsScreen from '../screens/main/QuantumOperationsScreen';
import ProfileScreen from '../screens/main/ProfileScreen';

// Business Pod Screens
import SigmaSelectScreen from '../screens/pods/SigmaSelectScreen';
import FlyFoxAIScreen from '../screens/pods/FlyFoxAIScreen';
import GoliathTradeScreen from '../screens/pods/GoliathTradeScreen';
import SFGSymmetryScreen from '../screens/pods/SFGSymmetryScreen';
import GhostNeuroQScreen from '../screens/pods/GhostNeuroQScreen';

// Settings Screens
import SettingsScreen from '../screens/settings/SettingsScreen';
import SecurityScreen from '../screens/settings/SecurityScreen';
import NotificationsScreen from '../screens/settings/NotificationsScreen';

export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
  Login: undefined;
  Register: undefined;
  BiometricSetup: undefined;
  PodDetail: { podId: string; podType: string };
  Settings: undefined;
  Security: undefined;
  Notifications: undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  BusinessPods: undefined;
  Operations: undefined;
  Profile: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

const AuthNavigator = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: theme.colors.primary,
      },
      headerTintColor: theme.colors.onPrimary,
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Stack.Screen 
      name="Login" 
      component={LoginScreen} 
      options={{ title: 'Welcome to FLYFOX AI' }}
    />
    <Stack.Screen 
      name="Register" 
      component={RegisterScreen} 
      options={{ title: 'Create Account' }}
    />
    <Stack.Screen 
      name="BiometricSetup" 
      component={BiometricSetupScreen} 
      options={{ title: 'Secure Your Account' }}
    />
  </Stack.Navigator>
);

const MainTabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ focused, color, size }) => {
        let iconName: string;

        switch (route.name) {
          case 'Dashboard':
            iconName = focused ? 'view-dashboard' : 'view-dashboard-outline';
            break;
          case 'BusinessPods':
            iconName = focused ? 'cube' : 'cube-outline';
            break;
          case 'Operations':
            iconName = focused ? 'atom' : 'atom-variant';
            break;
          case 'Profile':
            iconName = focused ? 'account' : 'account-outline';
            break;
          default:
            iconName = 'help-circle';
        }

        return <Icon name={iconName} size={size} color={color} />;
      },
      tabBarActiveTintColor: theme.colors.primary,
      tabBarInactiveTintColor: theme.colors.onSurfaceVariant,
      tabBarStyle: {
        backgroundColor: theme.colors.surface,
        borderTopColor: theme.colors.outline,
      },
      headerStyle: {
        backgroundColor: theme.colors.primary,
      },
      headerTintColor: theme.colors.onPrimary,
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    })}
  >
    <Tab.Screen 
      name="Dashboard" 
      component={DashboardScreen} 
      options={{ title: 'Quantum Dashboard' }}
    />
    <Tab.Screen 
      name="BusinessPods" 
      component={BusinessPodsScreen} 
      options={{ title: 'Business Pods' }}
    />
    <Tab.Screen 
      name="Operations" 
      component={QuantumOperationsScreen} 
      options={{ title: 'Quantum Ops' }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen} 
      options={{ title: 'Profile' }}
    />
  </Tab.Navigator>
);

const MainNavigator = () => (
  <Stack.Navigator
    screenOptions={{
      headerStyle: {
        backgroundColor: theme.colors.primary,
      },
      headerTintColor: theme.colors.onPrimary,
      headerTitleStyle: {
        fontWeight: 'bold',
      },
    }}
  >
    <Stack.Screen 
      name="Main" 
      component={MainTabNavigator} 
      options={{ headerShown: false }}
    />
    <Stack.Screen 
      name="PodDetail" 
      component={({ route }) => {
        const { podType } = route.params;
        switch (podType) {
          case 'SIGMA_SELECT':
            return <SigmaSelectScreen />;
          case 'FLYFOX_AI':
            return <FlyFoxAIScreen />;
          case 'GOLIATH_TRADE':
            return <GoliathTradeScreen />;
          case 'SFG_SYMMETRY':
            return <SFGSymmetryScreen />;
          case 'GHOST_NEUROQ':
            return <GhostNeuroQScreen />;
          default:
            return <DashboardScreen />;
        }
      }}
      options={({ route }) => ({
        title: route.params.podType.replace('_', ' '),
      })}
    />
    <Stack.Screen 
      name="Settings" 
      component={SettingsScreen} 
      options={{ title: 'Settings' }}
    />
    <Stack.Screen 
      name="Security" 
      component={SecurityScreen} 
      options={{ title: 'Security & Privacy' }}
    />
    <Stack.Screen 
      name="Notifications" 
      component={NotificationsScreen} 
      options={{ title: 'Notifications' }}
    />
  </Stack.Navigator>
);

const AppNavigator: React.FC = () => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {isAuthenticated ? (
        <Stack.Screen name="Main" component={MainNavigator} />
      ) : (
        <Stack.Screen name="Auth" component={AuthNavigator} />
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;