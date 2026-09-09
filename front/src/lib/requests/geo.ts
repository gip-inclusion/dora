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

/** Départements (nom + code) correspondant à une liste de codes de département. */
export async function getDepartments(
  departmentCodes: string[],
  fetchFunction = fetch
): Promise<DepartmentChoice[]> {
  const url = `${getApiURL()}/admin-division-departments/?dept_codes=${encodeURIComponent(
    departmentCodes.join(",")
  )}`;
  const response = await fetchFunction(url);
  const jsonResponse = (await response.json()) as GeoApiValue[];
  return jsonResponse.map((result) => ({
    value: result,
    label: `${result.name} (${result.code})`,
  }));
}
