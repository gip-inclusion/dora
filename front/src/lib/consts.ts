import { INCLUSION_PLATFORM_URL } from "$lib/env";

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

export const NATIONAL_ELIGIBLITITY_ZONE = "France entière";

export const MONTHS_BEFORE_OUTDATED = 6;

export const SEARCH_RADIUS_KM = 50;

// Durée de validité du lien de téléchargement de l'export des orientations
// (doit correspondre à `EXPORT_LINK_MAX_AGE` côté back)
export const ORIENTATIONS_EXPORT_LINK_VALIDITY_MINUTES = 10;

// Endpoint de recherche de la Base Adresse Nationale (BAN)
export const BAN_API_SEARCH_URL = "https://data.geopf.fr/geocodage/search/";

// Lien vers le formulaire permettant de signaler un problème dans les données de data·inclusion.
export const URL_MANAGER_DATA_INCLUSION_REPORT = "https://tally.so/r/nWZBrv";

// Lien vers le mode d'emploi du tableau de bord « Mes structures & services Dora » du gestionnaire de territoire
export const URL_MANAGER_HELP_NOTICE = `${URL_HELP_SITE}article/comment-utiliser-le-tableau-de-bord-de-gestionnaire-de-territoire-b5do49/`;

const AUTOMETA_DASHBOARDS_URL =
  "https://statistiques.inclusion.gouv.fr/dashboards";

// Tableau de bord Autometa public (lien « Statistiques » du footer)
export const AUTOMETA_PUBLIC_STATS_URL = `${AUTOMETA_DASHBOARDS_URL}/actes-metier-stats-publiques/`;

// Tableau de bord Autometa du gestionnaire de territoire, par département.
export const AUTOMETA_MANAGER_DASHBOARD_URLS = (departmentCode: string) => {
  const url = `${AUTOMETA_DASHBOARDS_URL}/tdb-gestionnaires-territoires/?dept=${departmentCode}`;

  return {
    accompagnements: `${url}&tab=accomp`,
    services: `${url}&tab=services`,
    structures: `${url}`,
  };
};

export const RATE_LIMIT_MESSAGE =
  "Vous avez effectué trop de requêtes. Veuillez patienter une minute avant de réessayer.";

export const PROCONNECT_MORE_INFO_URL = "https://www.proconnect.gouv.fr/";

// Page de connexion de la plateforme de l'inclusion, vers laquelle sont
// redirigés les professionnels de l'accompagnement.
export const INCLUSION_PLATFORM_LOGIN_URL = `${INCLUSION_PLATFORM_URL}/accounts/login?mtm_campaign=DORA&mtm_kwd=connexion`;

// Liens de la page d'accueil vers la recherche et le suivi des orientations
// de la plateforme de l'inclusion.
export const INCLUSION_PLATFORM_SEARCH_URL = `${INCLUSION_PLATFORM_URL}/search/services?mtm_campaign=DORA&mtm_kwd=homeorienter`;
export const INCLUSION_PLATFORM_ORIENTATIONS_URL = `${INCLUSION_PLATFORM_URL}/insertion/orientations/?mtm_campaign=DORA&mtm_kwd=homesuivi`;

export const ORIENTATION_JWT_QUERY_PARAM = "op";

export const TOAST_DURATION_MS = 30000;

// Messages d'erreur de chargement de chunk obsolète, propres à chaque
// navigateur : Chrome/Edge et Firefox pour le premier, Safari pour le second
export const STALE_CHUNK_ERROR_MESSAGES = [
  "dynamically imported module",
  "Importing a module script failed",
];

// Marqueur retourné par le handleError client lors du rechargement automatique
// après un déploiement, pour que la page d'erreur ne le remonte pas à Sentry
export const STALE_CHUNK_RELOAD_MESSAGE = "stale-chunk-reload";

// Message générique retourné par les handleError (client et serveur) en prod, en
// remplacement du message réel. L'erreur d'origine est déjà rapportée à Sentry par
// handleErrorWithSentry ; ce marqueur permet à la page d'erreur de ne pas la re-logger.
export const UNEXPECTED_ERROR_MESSAGE = "Erreur inattendue";
