export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export const PDF_SERVICE_URL =
  import.meta.env.VITE_PDF_SERVICE_URL || "http://localhost:8080/service-pdf";
export const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;
export const INTERNAL_API_URL = import.meta.env.VITE_INTERNAL_API_URL;
export const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN;
export const CANONICAL_URL = import.meta.env.VITE_CANONICAL_URL;
export const METABASE_EMBED_URL = import.meta.env.VITE_METABASE_EMBED_URL;
export const FLAG_STRIKING = import.meta.env.VITE_FLAG_STRIKING === "true";
