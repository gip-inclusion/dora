import { browser } from "$app/environment";
import { API_URL, INTERNAL_API_URL } from "$lib/env";

export function getApiURL() {
  if (browser) {
    return "/api";
  }
  return INTERNAL_API_URL || API_URL;
}

export const defaultAcceptHeader = "application/json; version=1.0";
