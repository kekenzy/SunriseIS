/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#0E1B2A',
          900: '#152534',
          800: '#1C3045',
        },
        teal: {
          600: '#2C7480',
          700: '#205E6A',
        },
        sand: '#D7D0C2',
      }
    }
  },
  plugins: []
}
