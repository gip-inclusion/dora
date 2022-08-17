const config = {
  use: {
    // Eviter les erreurs "Content Security Policy" des appels back-end
    bypassCSP: true,
  },
  webServer: {
    command: "npm run build:test && npm run preview",
    port: 3000,
  },
};

export default config;
