import type { GeoApiValue } from "../types";
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

export type DepartmentChoice = { value: GeoApiValue; label: string };

/**
 * Départements (nom + code) correspondant à une liste de codes de département,
 * ou `null` si l'appel a échoué (à distinguer d'une liste vide).
 */
export async function getDepartments(
  departmentCodes: string[],
  fetchFunction = fetch
): Promise<DepartmentChoice[] | null> {
  const url = `${getApiURL()}/admin-division-departments/?dept_codes=${encodeURIComponent(
    departmentCodes.join(",")
  )}`;

  const result = await fetchData<GeoApiValue[]>(url, fetchFunction);

  if (!result.ok) {
    return null;
  }

  return result.data.map((department) => ({
    value: department,
    label: `${department.name} (${department.code})`,
  }));
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
