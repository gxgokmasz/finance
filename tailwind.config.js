/** @type {import('tailwindcss').Config} */

const defaultTheme = require("tailwindcss/defaultTheme");

export default {
  content: ["./src/templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js"],
  safelist: ["charts"],
  theme: {
    extend: {},
    screens: {
      sm: "640px",
      "sm-md": "704px",
      md: "768px",
      "md-lg": "896px",
      lg: "1024px",
      "lg-xl": "1152px",
      xl: "1280px",
      "xl-2xl": "1408px",
      "2xl": "1536px",
    },
  },
  plugins: [
    require("flowbite/plugin")({
      charts: true,
    }),
  ],
};
