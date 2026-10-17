/** Tailwind for the v2 hand-built screens. Preflight is off: v1's captured app.css already ships it. */
module.exports = {
  content: ['./screens/**/*.html', './overlays/**/*.html', './router.js', './chat.js'],
  corePlugins: { preflight: false },
  theme: {
    extend: {
      fontFamily: { sans: ['"Inter var"', 'Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'] },
    },
  },
};
