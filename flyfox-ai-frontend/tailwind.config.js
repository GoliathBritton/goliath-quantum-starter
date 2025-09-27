/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        'black': '#000000',
        'silver': '#C0C0C0',
        'gold': '#FFD700',
        'dark-blue': '#00008B',
        'neutral': '#F5F5F5',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, #000000 0%, #00008B 100%)',
      },
      boxShadow: {
        'neon': '0 0 10px #FFD700, 0 0 20px #FFD700',
      },
    },
  },
  plugins: [],
}

