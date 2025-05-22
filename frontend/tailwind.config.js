/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./index.html"],
  theme: {
    extend: {},
  },
  plugins: [],
  // 与Ant Design兼容
  corePlugins: {
    preflight: false,
  },
} 