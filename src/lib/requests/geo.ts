import { getApiURL } from "../utils/api";
import { log } from "../utils/logger";
import { fetchData } from "../utils/misc";

export async function getCityLabel(inseeCode): Promise<string> {
  const url = `${getApiURL()}/city-label/${inseeCode}/`;
  const result = await fetchData<string>(url);
  if (result.ok) {
    return result.data;
  }
  log(
    `Impossible de trouver la ville correspondant au code INSEE ${inseeCode}`
  );
}
