import { browser } from "$app/environment";
import { API_URL } from "$lib/env";

export function getApiURL() {
  if (browser) {
    return "/api";
  }
  return API_URL;
}

export const defaultAcceptHeader = "application/json; version=1.0";
