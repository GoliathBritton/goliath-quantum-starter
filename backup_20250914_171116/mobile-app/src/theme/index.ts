import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

// Quantum-inspired color palette
const quantumColors = {
  // Primary quantum purple
  primary: '#8641F4',
  primaryContainer: '#E8D5FF',
  onPrimary: '#FFFFFF',
  onPrimaryContainer: '#2E004E',
  
  // Secondary quantum blue
  secondary: '#4A90E2',
  secondaryContainer: '#D1E4FF',
  onSecondary: '#FFFFFF',
  onSecondaryContainer: '#001D36',
  
  // Tertiary quantum teal
  tertiary: '#00BCD4',
  tertiaryContainer: '#B2EBF2',
  onTertiary: '#FFFFFF',
  onTertiaryContainer: '#002022',
  
  // Error states
  error: '#FF5252',
  errorContainer: '#FFEBEE',
  onError: '#FFFFFF',
  onErrorContainer: '#410E0B',
  
  // Success states
  success: '#4CAF50',
  successContainer: '#E8F5E8',
  onSuccess: '#FFFFFF',
  onSuccessContainer: '#1B5E20',
  
  // Warning states
  warning: '#FF9800',
  warningContainer: '#FFF3E0',
  onWarning: '#FFFFFF',
  onWarningContainer: '#E65100',
  
  // Surface colors
  surface: '#FFFFFF',
  surfaceVariant: '#F5F5F5',
  surfaceTint: '#8641F4',
  onSurface: '#1C1B1F',
  onSurfaceVariant: '#49454F',
  
  // Background
  background: '#FEFBFF',
  onBackground: '#1C1B1F',
  
  // Outline
  outline: '#79747E',
  outlineVariant: '#CAC4D0',
  
  // Inverse colors
  inverseSurface: '#313033',
  inverseOnSurface: '#F4EFF4',
  inversePrimary: '#D0BCFF',
  
  // Quantum-specific colors
  quantum: {
    entanglement: '#E91E63',
    superposition: '#9C27B0',
    coherence: '#673AB7',
    decoherence: '#FF5722',
    measurement: '#795548',
  },
  
  // Gradient colors
  gradients: {
    primary: ['#8641F4', '#4A90E2'],
    secondary: ['#4A90E2', '#00BCD4'],
    quantum: ['#8641F4', '#E91E63', '#00BCD4'],
    success: ['#4CAF50', '#8BC34A'],
    warning: ['#FF9800', '#FFC107'],
    error: ['#FF5252', '#F44336'],
  },
};

// Dark theme colors
const quantumDarkColors = {
  ...quantumColors,
  
  // Primary
  primary: '#D0BCFF',
  primaryContainer: '#4F378B',
  onPrimary: '#371E73',
  onPrimaryContainer: '#EADDFF',
  
  // Secondary
  secondary: '#CCC2DC',
  secondaryContainer: '#4A4458',
  onSecondary: '#332D41',
  onSecondaryContainer: '#E8DEF8',
  
  // Tertiary
  tertiary: '#EFB8C8',
  tertiaryContainer: '#633B48',
  onTertiary: '#492532',
  onTertiaryContainer: '#FFD8E4',
  
  // Surface colors
  surface: '#1C1B1F',
  surfaceVariant: '#49454F',
  onSurface: '#E6E1E5',
  onSurfaceVariant: '#CAC4D0',
  
  // Background
  background: '#141218',
  onBackground: '#E6E1E5',
  
  // Outline
  outline: '#938F99',
  outlineVariant: '#49454F',
  
  // Inverse colors
  inverseSurface: '#E6E1E5',
  inverseOnSurface: '#313033',
  inversePrimary: '#6750A4',
};

// Light theme
export const lightTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    ...quantumColors,
  },
};

// Dark theme
export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    ...quantumDarkColors,
  },
};

// Default theme (light)
export const theme = lightTheme;

// Typography
export const typography = {
  // Display styles
  displayLarge: {
    fontSize: 57,
    lineHeight: 64,
    fontWeight: '400' as const,
    letterSpacing: -0.25,
  },
  displayMedium: {
    fontSize: 45,
    lineHeight: 52,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  displaySmall: {
    fontSize: 36,
    lineHeight: 44,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  
  // Headline styles
  headlineLarge: {
    fontSize: 32,
    lineHeight: 40,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  headlineMedium: {
    fontSize: 28,
    lineHeight: 36,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  headlineSmall: {
    fontSize: 24,
    lineHeight: 32,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  
  // Title styles
  titleLarge: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '400' as const,
    letterSpacing: 0,
  },
  titleMedium: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '500' as const,
    letterSpacing: 0.15,
  },
  titleSmall: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500' as const,
    letterSpacing: 0.1,
  },
  
  // Body styles
  bodyLarge: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '400' as const,
    letterSpacing: 0.5,
  },
  bodyMedium: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '400' as const,
    letterSpacing: 0.25,
  },
  bodySmall: {
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '400' as const,
    letterSpacing: 0.4,
  },
  
  // Label styles
  labelLarge: {
    fontSize: 14,
    lineHeight: 20,
    fontWeight: '500' as const,
    letterSpacing: 0.1,
  },
  labelMedium: {
    fontSize: 12,
    lineHeight: 16,
    fontWeight: '500' as const,
    letterSpacing: 0.5,
  },
  labelSmall: {
    fontSize: 11,
    lineHeight: 16,
    fontWeight: '500' as const,
    letterSpacing: 0.5,
  },
};

// Spacing system
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
  xxxl: 64,
};

// Border radius
export const borderRadius = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  round: 9999,
};

// Shadows
export const shadows = {
  small: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  medium: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  large: {
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
  quantum: {
    shadowColor: quantumColors.primary,
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 12,
  },
};

// Animation durations
export const animations = {
  fast: 150,
  normal: 300,
  slow: 500,
  quantum: 800, // For quantum-themed animations
};

// Breakpoints for responsive design
export const breakpoints = {
  small: 0,
  medium: 768,
  large: 1024,
  xlarge: 1440,
};

// Z-index layers
export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
  toast: 1080,
};

export type Theme = typeof lightTheme;
export type ThemeColors = typeof quantumColors;
export type Typography = typeof typography;
export type Spacing = typeof spacing;
export type BorderRadius = typeof borderRadius;
export type Shadows = typeof shadows;
export type Animations = typeof animations;
export type Breakpoints = typeof breakpoints;
export type ZIndex = typeof zIndex;