/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'goliath-blue': '#1E40AF',
        'goliath-gold': '#F59E0B',
        'goliath-silver': '#6B7280',
        'goliath-bronze': '#D97706',
        'goliath-platinum': '#94A3B8',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
