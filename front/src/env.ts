import { defineEnvVars } from "@sveltejs/kit/env";

export const variables = defineEnvVars({
  MAX_REQUESTS_PER_MINUTE: {
    // Inlinée au build, comme l'ancien `$env/static/private`
    static: true,
    schema: (value) => Number(value) || 24,
    description:
      "Nombre maximum de requêtes par minute et par couple IP/User-Agent",
  },
  VITE_PUBLIC_CANONICAL_URL: {
    // Utilisée dans `src/app.html` (`%sveltekit.env.VITE_PUBLIC_CANONICAL_URL%`)
    public: true,
    description: "URL canonique du site",
  },
  VITE_PUBLIC_MATOMO_CONTAINER_URL: {
    // Utilisée dans `src/app.html` (`%sveltekit.env.VITE_PUBLIC_MATOMO_CONTAINER_URL%`)
    // Optionnelle : le script Matomo n'est pas chargé si elle est absente
    public: true,
    schema: (value) => value ?? "",
    description: "URL du conteneur de balises Matomo",
  },
  FRONT_PROXY_SECRET: {
    schema: (value) => value,
    description:
      "Secret partagé avec le back, authentifiant l'IP du client relayée par le front",
  },
});
