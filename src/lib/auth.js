import { writable } from "svelte/store";
import { browser } from "$app/env";
import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";

const tokenKey = "token";

export const token = writable(null);

export function setToken(t) {
  token.set(t);
  localStorage.setItem(tokenKey, t);
}

export function clearToken() {
  token.set(null);
  localStorage.removeItem(tokenKey);
}

export async function initToken() {
  token.set(null);
  if (browser) {
    const lsToken = localStorage.getItem(tokenKey);
    if (lsToken) {
      // Check if the token is still valid
      const url = `${getApiURL()}/auth/token/verify/`;
      const result = await fetch(url, {
        method: "POST",
        headers: {
          Accept: defaultAcceptHeader,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ key: lsToken }),
      });
      if (result.ok) {
        token.set(lsToken);
      }
      if (!result.ok && result.status === 404) {
        // The token is invalid, clear localStorage
        clearToken();
      }
    }
  }
}
