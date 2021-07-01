import { browser } from "$app/env";

import { API_URL, INTERNAL_API_URL } from "$lib/env.js";

export function getApiURL() {
  if (browser || !INTERNAL_API_URL) return API_URL;
  return INTERNAL_API_URL;
}
