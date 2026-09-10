import { getApiURL } from "../utils/api";
import { log } from "../utils/logger";
import { fetchData } from "../utils/misc";

export async function getCityLabel(
  inseeCode: string,
  fetchFunction = fetch
): Promise<string | null> {
  // Validation simple du code INSEE (que des chiffres)
  if (!inseeCode || !/^[0-9]+$/.test(inseeCode.trim())) {
    log(`Code INSEE invalide: ${inseeCode}`);
    return null;
  }

  const cleanInseeCode = inseeCode.trim();
  const url = `${getApiURL()}/city-label/${cleanInseeCode}/`;

  const result = await fetchData<string>(url, fetchFunction);

  return result.ok ? result.data : null;
}

export interface EpcisAndCitiesResults {
  // pour une commune le code INSEE, pour un EPCI ses codes de départements
  cities: Array<{ label: string; value: string }>;
  epcis: Array<{ label: string; value: string[] }>;
}

export async function searchEpcisAndCities(
  query: string,
  fetchFunction = fetch
): Promise<EpcisAndCitiesResults | null> {
  const url = `${getApiURL()}/admin-division-search-epcis-cities/?q=${encodeURIComponent(query)}`;

  const result = await fetchData<EpcisAndCitiesResults>(url, fetchFunction);

  return result.ok ? result.data : null;
}
