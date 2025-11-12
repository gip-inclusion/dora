export const SIREN_FRANCE_TRAVAIL = "130005481";

export const enum TallyFormId {
  NOTEBOOK_ORDER_FORM_ID = "mRMDWl",
  SERVICE_CREATION_FORM_ID = "mRGdpK",
}

export const TEST_WORDS = ["test", "truc", "bidule"];

export const URL_DOCUMENTATION_ORIENTATION =
  "https://aide.dora.inclusion.beta.gouv.fr/fr/category/orienter-vos-beneficiaires-c25cna/";

export const SITEMAP_PAGE_SIZE = 1000;

export const MON_RECAP_DEPARTMENTS = ["59", "69", "93"];

export const METABASE_DASHBOARD_URL = (departmentCode: string) =>
  `https://metabase.dora.inclusion.gouv.fr/public/dashboard/cac884d0-fdeb-4d69-b1cc-9ae58a4cd32f?d%25C3%25A9partement_de_la_structure=${departmentCode}`;

export const DI_METABASE_DASHBOARD_URL = (departmentName: string) =>
  `https://stats.inclusion.beta.gouv.fr/public/dashboard/9a839a8a-2af2-4593-a800-1a67661247e8?d%25C3%25A9partement=${departmentName}`;

export const RATE_LIMIT_MESSAGE =
  "Vous avez effectué trop de requêtes. Veuillez patienter une minute avant de réessayer.";

export const MOBILE_BREAKPOINT = 768; // 'md' from https://tailwindcss.com/docs/screens
