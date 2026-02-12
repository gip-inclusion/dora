export const SIREN_FRANCE_TRAVAIL = "130005481";

export const enum TallyFormId {
  NOTEBOOK_ORDER_FORM_ID = "mRMDWl",
  SERVICE_CREATION_FORM_ID = "mRGdpK",
}

export const TEST_WORDS = ["test", "truc", "bidule"];

export const URL_HELP_SITE = "https://aide.dora.inclusion.gouv.fr/fr/";

export const URL_DOCUMENTATION_ORIENTATION = `${URL_HELP_SITE}category/orienter-vos-beneficiaires-c25cna/`;

export const SITEMAP_PAGE_SIZE = 1000;

export const MON_RECAP_DEPARTMENTS = ["59", "69", "93"];

export const SEARCH_RADIUS_KM = 50;

export const METABASE_DASHBOARD_URL = (departmentCode: string) =>
  `https://metabase.dora.inclusion.gouv.fr/public/dashboard/cac884d0-fdeb-4d69-b1cc-9ae58a4cd32f?d%25C3%25A9partement_de_la_structure=${departmentCode}`;

export const DI_METABASE_STATS_DASHBOARD_URL = (
  departmentName: string,
  dataSource: string = "dora"
) =>
  `https://stats.inclusion.beta.gouv.fr/public/dashboard/bbe6a581-0ecc-40cb-84d3-b3f2e9625f5b?d%25C3%25A9partement=${departmentName}&producteur_de_donn%25C3%25A9es=${dataSource}`;

export const DI_METABASE_LIST_DASHBOARD_URL = (
  departmentName: string,
  dataSource: string = "dora"
) =>
  `https://stats.inclusion.beta.gouv.fr/public/dashboard/e5baef58-cc06-4c9c-aec4-5919654b2534?d%25C3%25A9partement=${departmentName}&producteur_de_donn%25C3%25A9es=${dataSource}`;

export const RATE_LIMIT_MESSAGE =
  "Vous avez effectué trop de requêtes. Veuillez patienter une minute avant de réessayer.";

export const EMPLOIS_MORE_INFO_URL =
  "https://aide.emplois.inclusion.beta.gouv.fr/hc/fr/articles/14738715340177--M-inscrire-sur-les-emplois-de-l-inclusion-en-tant-que-SIAE";
