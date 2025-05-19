export default {
  plugins: [
    // ⬇️ use the new PostCSS plugin
    require("@tailwindcss/postcss")(),
    require("autoprefixer")(),
  ],
};
