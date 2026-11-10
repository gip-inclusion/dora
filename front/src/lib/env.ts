export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;
export const SENTRY_DSN = import.meta.env.VITE_SENTRY_DSN;
export const CANONICAL_URL = import.meta.env.VITE_PUBLIC_CANONICAL_URL;
export const WARNING_BANNER = import.meta.env.VITE_WARNING_BANNER;
export const OIDC_AUTH_BACKEND =
  import.meta.env.VITE_OIDC_AUTH_BACKEND || "proconnect";
export const INCLUSION_PLATFORM_URL =
  import.meta.env.VITE_INCLUSION_PLATFORM_URL ||
  "https://plateforme.inclusion.gouv.fr";
export const ORIENTATION_REDIRECTION_FEATURE_FLAG =
  import.meta.env.VITE_ORIENTATION_REDIRECTION_FEATURE_FLAG === "true";
