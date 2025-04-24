import { API_URL } from "$lib/env";
import { log } from "../utils/logger";
import { fetchData } from "../utils/misc";

export async function getCityLabel(inseeCode): Promise<string> {
  const url = `${API_URL}/city-label/${inseeCode}/`;
  const result = await fetchData<string>(url);
  if (result.ok) {
    return result.data;
  }
  log(
    `Impossible de trouver la ville correspondant au code INSEE ${inseeCode}`
  );
  return "";
}
