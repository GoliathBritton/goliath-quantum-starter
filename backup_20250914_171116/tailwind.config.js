/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // FLYFOX AI Brand Colors
        'flyfox-navy': '#0f172a',
        'goliath-gold': '#F59E0B',
        'sigma-purple': '#7C3AED',
        'quantum-cyan': '#06B6D4',
        'muted-ink': '#111827',
        flyfox: {
          DEFAULT: '#00FF88', // Energy Green - Primary brand color
          50: '#f0fdf9',
          100: '#ccfbef',
          200: '#99f6e0',
          300: '#5eead4',
          400: '#2dd4bf',
          500: '#00FF88', // Primary
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        quantum: {
          DEFAULT: '#0066CC', // Quantum Blue - Trust, technology
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#0066CC', // Primary
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        premium: {
          DEFAULT: '#FFD700', // Premium Gold - Luxury, value
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#FFD700', // Primary
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        space: {
          DEFAULT: '#1A1A2E', // Deep Space - Sophistication
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#1A1A2E', // Primary
        },
        // Quantum-themed gradients
        'quantum-gradient': {
          from: '#0f0f1f',
          via: '#3b0764',
          to: '#0d9488',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      animation: {
        'gradient-x': 'gradient-x 12s ease infinite',
        'quantum-pulse': 'quantum-pulse 2s ease-in-out infinite',
        'quantum-glow': 'quantum-glow 3s ease-in-out infinite',
        'quantum-float': 'quantum-float 4s ease-in-out infinite',
        'spin-slow': 'spin 3s linear infinite',
      },
      keyframes: {
        'gradient-x': {
          '0%, 100%': {
            'background-position': '0% 50%',
          },
          '50%': {
            'background-position': '100% 50%',
          },
        },
        'quantum-pulse': {
          '0%, 100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
          '50%': {
            opacity: '0.8',
            transform: 'scale(1.05)',
          },
        },
        'quantum-glow': {
          '0%, 100%': {
            'box-shadow': '0 0 5px rgba(139, 92, 246, 0.3)',
          },
          '50%': {
            'box-shadow': '0 0 20px rgba(139, 92, 246, 0.6), 0 0 30px rgba(20, 184, 166, 0.4)',
          },
        },
        'quantum-float': {
          '0%, 100%': {
            transform: 'translateY(0px) rotate(0deg)',
          },
          '33%': {
            transform: 'translateY(-10px) rotate(120deg)',
          },
          '66%': {
            transform: 'translateY(5px) rotate(240deg)',
          },
        },
      },
      backgroundImage: {
        'quantum-gradient': 'linear-gradient(-45deg, #0f0f1f, #3b0764, #0d9488, #1e293b)',
        'flyfox-gradient': 'linear-gradient(135deg, #00FF88, #0066CC)',
        'premium-gradient': 'linear-gradient(135deg, #FFD700, #FFA500)',
        'hero-gradient': 'linear-gradient(135deg, #0f172a, #06B6D4)',
        'glassmorphism': 'rgba(255, 255, 255, 0.1)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};