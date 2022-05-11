module.exports = {
  content: ["./src/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        raleway: ["Raleway", "sans-serif"],
      }
    },
  },
  plugins: [],
  safelist: [
    {
      pattern : /bg-(red|green|blue|yellow)-(700)/,
    },
    "bg-gradient-to-r from-pink-500 via-red-500 to-yellow-500",
    "bg-gradient-to-r from-green-300 via-blue-500 to-purple-600",
    "bg-gradient-to-r from-pink-300 via-purple-300 to-indigo-400",
    "bg-gradient-to-r from-gray-700 via-gray-900 to-black",
    "bg-gradient-to-r from-indigo-200 via-red-200 to-yellow-100",
    "bg-gradient-to-r from-yellow-100 via-yellow-300 to-yellow-500"
  ]
}
