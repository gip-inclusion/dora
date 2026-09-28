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

export const MONTHS_BEFORE_OUTDATED = 6;

export const SEARCH_RADIUS_KM = 50;

// Endpoint de recherche de la Base Adresse Nationale (BAN)
export const BAN_API_SEARCH_URL = "https://data.geopf.fr/geocodage/search/";

// Lien vers l'article expliquant le rôle de gestionnaire de territoire, affichée sur la page d'accueil « Gérer mon territoire »
export const URL_MANAGER_HELP_NOTICE = `${URL_HELP_SITE}article/quest-ce-quun-profil-gestionnaire-de-territoire-16sn5g2/`;

// Lien vers l'article (encore à créer) expliquant comment signaler un problème dans les données de data·inclusion.
export const URL_MANAGER_DATA_INCLUSION_NOTICE = URL_HELP_SITE;

// Lien vers le mode d'emploi du tableau de bord « Mes structures & services Dora » du gestionnaire de territoire
export const URL_MANAGER_DASHBOARD_HELP_NOTICE = `${URL_HELP_SITE}article/comment-utiliser-le-tableau-de-bord-de-gestionnaire-de-territoire-b5do49/`;

// Tableau de bord Autometa du gestionnaire de territoire, par département.
export const AUTOMETA_MANAGER_DASHBOARD_URLS = (departmentCode: string) => {
  const url = `https://statistiques.inclusion.gouv.fr/dashboards/tdb-gestionnaires-territoires/?dept=${departmentCode}`;

  return {
    accompagnements: `${url}&tab=accomp`,
    services: `${url}&tab=services`,
    structures: `${url}`,
  };
};

export const RATE_LIMIT_MESSAGE =
  "Vous avez effectué trop de requêtes. Veuillez patienter une minute avant de réessayer.";

export const EMPLOIS_MORE_INFO_URL =
  "https://aide.emplois.inclusion.beta.gouv.fr/hc/fr/articles/14738715340177--M-inscrire-sur-les-emplois-de-l-inclusion-en-tant-que-SIAE";

export const PROCONNECT_MORE_INFO_URL = "https://www.proconnect.gouv.fr/";

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
