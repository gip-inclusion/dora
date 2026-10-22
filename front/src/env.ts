import { defineEnvVars } from "@sveltejs/kit/env";

export const variables = defineEnvVars({
  MAX_REQUESTS_PER_MINUTE: {
    // Inlinée au build, comme l'ancien `$env/static/private`
    static: true,
    schema: (value) => Number(value) || 24,
    description:
      "Nombre maximum de requêtes par minute et par couple IP/User-Agent",
  },
  FRONT_PROXY_SECRET: {
    schema: (value) => value,
    description:
      "Secret partagé avec le back, authentifiant l'IP du client relayée par le front",
  },
  SNAPSHOT_SECRET: {
    schema: (value) => value,
    description:
      "Secret protégeant l'endpoint de capture de l'empreinte mémoire",
  },
});
