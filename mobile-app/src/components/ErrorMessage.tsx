import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Text, Button, IconButton } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { theme } from '../theme';

interface ErrorMessageProps {
  message: string;
  title?: string;
  onRetry?: () => void;
  onDismiss?: () => void;
  retryText?: string;
  dismissible?: boolean;
  type?: 'error' | 'warning' | 'info';
  quantum?: boolean;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({
  message,
  title,
  onRetry,
  onDismiss,
  retryText = 'Retry',
  dismissible = true,
  type = 'error',
  quantum = false,
}) => {
  const getIconName = () => {
    switch (type) {
      case 'warning':
        return 'alert';
      case 'info':
        return 'information';
      default:
        return quantum ? 'atom-variant' : 'alert-circle';
    }
  };

  const getIconColor = () => {
    switch (type) {
      case 'warning':
        return theme.colors.warning;
      case 'info':
        return theme.colors.primary;
      default:
        return theme.colors.error;
    }
  };

  const getBackgroundColor = () => {
    switch (type) {
      case 'warning':
        return theme.colors.warningContainer;
      case 'info':
        return theme.colors.primaryContainer;
      default:
        return theme.colors.errorContainer;
    }
  };

  const getTextColor = () => {
    switch (type) {
      case 'warning':
        return theme.colors.onWarningContainer;
      case 'info':
        return theme.colors.onPrimaryContainer;
      default:
        return theme.colors.onErrorContainer;
    }
  };

  const getDefaultTitle = () => {
    if (quantum) {
      switch (type) {
        case 'warning':
          return 'Quantum Decoherence Warning';
        case 'info':
          return 'Quantum Information';
        default:
          return 'Quantum Error Detected';
      }
    }
    
    switch (type) {
      case 'warning':
        return 'Warning';
      case 'info':
        return 'Information';
      default:
        return 'Error';
    }
  };

  return (
    <Card 
      style={[
        styles.container,
        { backgroundColor: getBackgroundColor() }
      ]}
    >
      <Card.Content>
        <View style={styles.header}>
          <View style={styles.titleContainer}>
            <Icon 
              name={getIconName()} 
              size={24} 
              color={getIconColor()}
              style={styles.icon}
            />
            <Text 
              style={[
                styles.title,
                { color: getTextColor() }
              ]}
            >
              {title || getDefaultTitle()}
            </Text>
          </View>
          
          {dismissible && onDismiss && (
            <IconButton
              icon="close"
              size={20}
              iconColor={getTextColor()}
              onPress={onDismiss}
              style={styles.dismissButton}
            />
          )}
        </View>
        
        <Text 
          style={[
            styles.message,
            { color: getTextColor() }
          ]}
        >
          {message}
        </Text>
        
        {quantum && (
          <Text 
            style={[
              styles.quantumNote,
              { color: getTextColor() }
            ]}
          >
            Quantum state may have been affected. Please try again.
          </Text>
        )}
        
        {onRetry && (
          <View style={styles.actions}>
            <Button
              mode="contained"
              onPress={onRetry}
              style={[
                styles.retryButton,
                { backgroundColor: getIconColor() }
              ]}
              labelStyle={{ color: 'white' }}
              icon={quantum ? 'atom' : 'refresh'}
            >
              {quantum ? 'Reinitialize Quantum State' : retryText}
            </Button>
          </View>
        )}
      </Card.Content>
    </Card>
  );
};

const styles = StyleSheet.create({
  container: {
    margin: 16,
    elevation: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  icon: {
    marginRight: 8,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    flex: 1,
  },
  dismissButton: {
    margin: 0,
    marginTop: -8,
    marginRight: -8,
  },
  message: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 8,
  },
  quantumNote: {
    fontSize: 12,
    fontStyle: 'italic',
    marginBottom: 16,
    opacity: 0.8,
  },
  actions: {
    marginTop: 8,
  },
  retryButton: {
    alignSelf: 'flex-start',
  },
});

export default ErrorMessage;