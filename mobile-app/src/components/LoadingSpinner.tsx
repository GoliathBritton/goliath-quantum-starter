import React from 'react';
import { View, StyleSheet } from 'react-native';
import { ActivityIndicator, Text, Surface } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { theme } from '../theme';

interface LoadingSpinnerProps {
  message?: string;
  size?: 'small' | 'large';
  quantum?: boolean;
  overlay?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 'large',
  quantum = true,
  overlay = false,
}) => {
  const containerStyle = overlay ? styles.overlayContainer : styles.container;

  return (
    <View style={containerStyle}>
      <Surface style={styles.surface}>
        <View style={styles.content}>
          {quantum ? (
            <View style={styles.quantumLoader}>
              <Icon 
                name="atom" 
                size={size === 'large' ? 48 : 32} 
                color={theme.colors.primary} 
                style={styles.quantumIcon}
              />
              <ActivityIndicator 
                size={size} 
                color={theme.colors.secondary}
                style={styles.spinner}
              />
            </View>
          ) : (
            <ActivityIndicator 
              size={size} 
              color={theme.colors.primary}
            />
          )}
          
          {message && (
            <Text style={styles.message}>
              {message}
            </Text>
          )}
          
          {quantum && (
            <Text style={styles.quantumText}>
              Quantum processing...
            </Text>
          )}
        </View>
      </Surface>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
  },
  overlayContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 1000,
  },
  surface: {
    padding: 32,
    borderRadius: 16,
    elevation: 8,
    backgroundColor: theme.colors.surface,
  },
  content: {
    alignItems: 'center',
  },
  quantumLoader: {
    position: 'relative',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
  },
  quantumIcon: {
    position: 'absolute',
    zIndex: 1,
  },
  spinner: {
    transform: [{ scale: 1.5 }],
  },
  message: {
    marginTop: 16,
    fontSize: 16,
    textAlign: 'center',
    color: theme.colors.onSurface,
  },
  quantumText: {
    marginTop: 8,
    fontSize: 12,
    textAlign: 'center',
    color: theme.colors.primary,
    fontStyle: 'italic',
  },
});

export default LoadingSpinner;