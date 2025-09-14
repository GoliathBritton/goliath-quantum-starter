import React, { Component, ReactNode } from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph, Button, Surface } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { theme } from '../theme';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: any;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    this.setState({
      error,
      errorInfo,
    });

    // Log error to crash reporting service
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <View style={styles.container}>
          <Surface style={styles.surface}>
            <Card style={styles.card}>
              <Card.Content>
                <View style={styles.header}>
                  <Icon 
                    name="alert-circle" 
                    size={48} 
                    color={theme.colors.error} 
                    style={styles.icon}
                  />
                  <Title style={styles.title}>Something went wrong</Title>
                </View>
                
                <Paragraph style={styles.message}>
                  An unexpected error occurred in the FLYFOX AI Platform. 
                  Our quantum systems are working to resolve this issue.
                </Paragraph>
                
                {__DEV__ && this.state.error && (
                  <View style={styles.debugInfo}>
                    <Paragraph style={styles.debugTitle}>Debug Information:</Paragraph>
                    <Paragraph style={styles.debugText}>
                      {this.state.error.toString()}
                    </Paragraph>
                    {this.state.errorInfo && (
                      <Paragraph style={styles.debugText}>
                        {this.state.errorInfo.componentStack}
                      </Paragraph>
                    )}
                  </View>
                )}
                
                <View style={styles.actions}>
                  <Button 
                    mode="contained" 
                    onPress={this.handleRetry}
                    style={styles.retryButton}
                    icon="refresh"
                  >
                    Try Again
                  </Button>
                </View>
              </Card.Content>
            </Card>
          </Surface>
        </View>
      );
    }

    return this.props.children;
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
    padding: 16,
  },
  surface: {
    borderRadius: 16,
    elevation: 8,
    maxWidth: 400,
    width: '100%',
  },
  card: {
    backgroundColor: theme.colors.surface,
  },
  header: {
    alignItems: 'center',
    marginBottom: 16,
  },
  icon: {
    marginBottom: 8,
  },
  title: {
    textAlign: 'center',
    color: theme.colors.onSurface,
    fontSize: 20,
    fontWeight: 'bold',
  },
  message: {
    textAlign: 'center',
    color: theme.colors.onSurface,
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 16,
  },
  debugInfo: {
    backgroundColor: theme.colors.errorContainer,
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  debugTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: theme.colors.onErrorContainer,
    marginBottom: 8,
  },
  debugText: {
    fontSize: 12,
    color: theme.colors.onErrorContainer,
    fontFamily: 'monospace',
  },
  actions: {
    alignItems: 'center',
  },
  retryButton: {
    backgroundColor: theme.colors.primary,
  },
});

export default ErrorBoundary;