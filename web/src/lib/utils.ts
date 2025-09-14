import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Utility for formatting numbers with quantum-themed suffixes
export function formatQuantumNumber(num: number): string {
  if (num >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
  if (num >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
  if (num >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
  if (num >= 1e3) return `${(num / 1e3).toFixed(2)}K`;
  return num.toFixed(2);
}

// Utility for generating quantum-themed colors
export function getQuantumColor(index: number): string {
  const colors = [
    '#0ea5e9', // sky-500
    '#d946ef', // fuchsia-500
    '#10b981', // emerald-500
    '#f59e0b', // amber-500
    '#ef4444', // red-500
    '#8b5cf6', // violet-500
    '#06b6d4', // cyan-500
    '#84cc16', // lime-500
  ];
  return colors[index % colors.length];
}

// Utility for debouncing functions
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

// Utility for throttling functions
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Utility for generating random quantum-themed IDs
export function generateQuantumId(): string {
  const prefixes = ['qbit', 'quant', 'flux', 'wave', 'spin', 'entgl'];
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
  const suffix = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${suffix}`;
}

// Utility for validating quantum circuit parameters
export function validateQuantumParams(params: Record<string, any>): boolean {
  const requiredFields = ['qubits', 'depth'];
  return requiredFields.every(field => 
    params[field] !== undefined && 
    params[field] !== null && 
    typeof params[field] === 'number' && 
    params[field] > 0
  );
}

// Utility for formatting time durations
export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  if (ms < 3600000) return `${(ms / 60000).toFixed(1)}m`;
  return `${(ms / 3600000).toFixed(1)}h`;
}

// Utility for calculating quantum fidelity color
export function getFidelityColor(fidelity: number): string {
  if (fidelity >= 0.95) return '#10b981'; // emerald-500
  if (fidelity >= 0.85) return '#f59e0b'; // amber-500
  if (fidelity >= 0.7) return '#ef4444';  // red-500
  return '#6b7280'; // gray-500
}

// Utility for generating quantum noise simulation
export function generateQuantumNoise(amplitude: number = 0.1): number {
  return (Math.random() - 0.5) * 2 * amplitude;
}

// Utility for quantum state probability calculation
export function calculateStateProbability(amplitude: { real: number; imag: number }): number {
  return amplitude.real * amplitude.real + amplitude.imag * amplitude.imag;
}