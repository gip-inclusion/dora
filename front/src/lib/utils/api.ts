import { browser } from "$app/env";
import { API_URL } from "#lib/env.ts";

export function getApiURL() {
  if (browser) {
    return "/api";
  }
  return API_URL;
}

export const defaultAcceptHeader = "application/json; version=1.0";
