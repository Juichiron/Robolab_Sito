/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'background-primary': '#262626',
        'background-secondary': '#383838',
        'accent': '#e74c3c',
        'primary': '#ffc812',
        'secondary': '#ffd447',
        'background-primary-light': '#cdcdcd',
        'text-color': '#f0efef',
      },
    },
  },
  plugins: [],
}

