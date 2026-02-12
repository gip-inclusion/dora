export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;
export const INTERNAL_API_URL = import.meta.env.VITE_INTERNAL_API_URL;
export const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN;
export const CANONICAL_URL = import.meta.env.VITE_PUBLIC_CANONICAL_URL;
export const METABASE_EMBED_URL = import.meta.env.VITE_METABASE_EMBED_URL;
export const WARNING_BANNER = import.meta.env.VITE_WARNING_BANNER;
export const OIDC_AUTH_BACKEND =
  import.meta.env.VITE_OIDC_AUTH_BACKEND || "proconnect";
export const GOOGLE_CSE_ID = import.meta.env.VITE_GOOGLE_CSE_ID;
export const DI_DORA_UNIFIED_SEARCH_ENABLED =
  import.meta.env.VITE_DI_DORA_UNIFIED_SEARCH_ENABLED !== "false";
export const EMPLOIS_SIGNUP_PAGE_URL = import.meta.env
  .VITE_EMPLOIS_SIGNUP_PAGE_URL;
