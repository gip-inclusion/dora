import { getApiURL } from "../utils/api";
import { log } from "../utils/logger";
import { fetchData } from "../utils/misc";

export async function getCityLabel(
  inseeCode: string,
  fetch = window.fetch
): Promise<string | null> {
  // Validation simple du code INSEE (que des chiffres)
  if (!inseeCode || !/^[0-9]+$/.test(inseeCode.trim())) {
    log(`Code INSEE invalide: ${inseeCode}`);
    return null;
  }

  const cleanInseeCode = inseeCode.trim();
  const url = new URL(`city-label/${cleanInseeCode}/`, getApiURL()).toString();

  const result = await fetchData<string>(url, fetch);

  return result.ok ? result.data : null;
}
