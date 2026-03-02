/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        gray: {
          850: '#1f2937',
          900: '#111827',
          950: '#030712',
        },
        // Custom Jarvis Palette (Clean Light Theme) - Kept for backward compatibility
        jarvis: {
          bg: "#f8fafc",       // Slate 50 (App Background)
          surface: "#ffffff",  // White (Card/Panel Background)
          border: "#e2e8f0",   // Slate 200 (Borders)
          text: "#1e293b",     // Slate 800 (Primary Text)
          dimmed: "#64748b",   // Slate 500 (Secondary Text)
          primary: "#6366f1",  // Indigo 500 (Brand Color)
          accent: "#f43f5e",   // Rose 500 (Alerts)
          success: "#10b981",  // Emerald 500 (Success)
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
