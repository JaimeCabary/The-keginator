// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9', // Refined blue
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        solana: {
          purple: '#9945FF',
          green: '#14F195',
          cyan: '#00FFD1',
          dark: {
            purple: '#7A36CC',
            green: '#10C177',
            cyan: '#00CCAA',
          }
        },
        dark: {
          100: '#0a0a0a',
          200: '#1a1a1a',
          300: '#2d2d2d',
          400: '#404040',
          500: '#525252',
        }
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'terminal-typing': 'typing 3.5s steps(40, end)',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%': { boxShadow: '0 0 20px rgba(153, 69, 255, 0.3)' }, // Solana purple
          '100%': { boxShadow: '0 0 30px rgba(153, 69, 255, 0.6)' },
        }
      },
      backgroundImage: {
        'grid-pattern': 'linear-gradient(rgba(153, 69, 255, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(153, 69, 255, 0.1) 1px, transparent 1px)',
        'space-gradient': 'radial-gradient(ellipse at top, rgba(153, 69, 255, 0.15), transparent), radial-gradient(ellipse at bottom, rgba(20, 241, 149, 0.15), transparent)',
      }
    },
  },
  plugins: [],
}