// Depuis la v11 du SDK Sentry, `sendDefaultPii` est remplacé par `dataCollection`,
// qui collecte tout par défaut (cookies, corps de requêtes, infos utilisateur…).
// On fixe explicitement les valeurs par défaut de la v10 (`sendDefaultPii` absent)
// pour ne pas envoyer davantage de données personnelles à Sentry.
// cf. https://docs.sentry.io/platforms/javascript/migration/v10-to-v11/#data-collection
const PII_HEADER_DENYLIST = ["forwarded", "-ip", "remote-", "via", "-user"];

export const SENTRY_DATA_COLLECTION = {
  userInfo: false,
  cookies: false,
  httpHeaders: {
    request: { deny: PII_HEADER_DENYLIST },
    response: { deny: PII_HEADER_DENYLIST },
  },
  httpBodies: [],
  urlQueryParams: { deny: PII_HEADER_DENYLIST },
  genAI: { inputs: false, outputs: false },
  databaseQueryData: false,
  graphQL: { document: false, variables: false },
};
