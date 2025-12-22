import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

interface CityResult {
  city: string;
  zip_code: string;
  slug: string;
  slug_alias: string | null;
  region: string;
}

function redirectToCollectiviteFr(citySlug = "") {
  redirect(
    307,
    // Page d'accueil si le slug de la ville n'a pas été déterminé
    // Page de la ville si le slug a été déterminé
    `https://collectivite.fr/${citySlug}?mtm_campaign=backlink_SE_dora`
  );
}

async function searchCitySlug(
  cityName: string,
  departmentCode: string,
  fetchFunction: typeof fetch
) {
  // Recherche du nom de la ville sur l'API de collectivites.fr
  const response = await fetchFunction(
    `https://api.collectivite.fr/api/commune/search/${cityName}`
  );
  const results = (await response.json()) as CityResult[];

  // Prise en compte du premier résultat correspondant au département
  const firstMatchingResult = results.find((result) =>
    result.zip_code.startsWith(departmentCode)
  );

  // Prise en compte du slug_alias ou du slug
  // Si aucun résultat ne correspond, retour d'un slug vide
  return firstMatchingResult?.slug_alias || firstMatchingResult?.slug || "";
}

export const load: PageLoad = async ({ fetch, url }) => {
  const query = url.searchParams;
  const cityLabel = query.get("cl");

  // Isolation du nom de la ville et du code du département
  const cityMatchGroups = cityLabel?.match(/(.+) \((.+)\)/);

  if (!cityMatchGroups) {
    // Si cityLabel n'est pas fourni ou est invalide, redirection vers la page d'accueil de collectivite.fr
    redirectToCollectiviteFr();
    return;
  }

  const cityName = cityMatchGroups[1];
  const departmentCode = cityMatchGroups[2];

  let citySlug: string;
  try {
    // Recherche du slug correspondant à la ville et au département
    citySlug = await searchCitySlug(cityName, departmentCode, fetch);
  } catch {
    citySlug = "";
  }

  // Redirection vers la page de la ville de collectivite.fr
  redirectToCollectiviteFr(citySlug);
};
