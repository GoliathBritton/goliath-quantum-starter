import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-paper';
import LoadingSpinner from './LoadingSpinner';
import { theme } from '../theme';

interface LoadingScreenProps {
  message?: string;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ 
  message = 'Initializing FLYFOX AI Platform...' 
}) => {
  return (
    <View style={styles.container}>
      <LoadingSpinner 
        message={message}
        size="large"
        quantum={true}
        overlay={false}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
});

export default LoadingScreen;