/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          light: '#fde047', // Dourado claro
          DEFAULT: '#eab308', // Dourado base
          dark: '#ca8a04', // Dourado escuro
          bg: '#0f172a', // Background principal escuro
          surface: '#1e293b', // Background para cards
          border: '#334155'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
