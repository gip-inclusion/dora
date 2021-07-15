import { browser } from "$app/env";
import { writable } from "svelte/store";

const tokenKey = "token";

export const token = writable(getToken());

function getToken() {
  if (browser) return localStorage.getItem(tokenKey);
  return null;
}

export function setToken(t) {
  localStorage.setItem(tokenKey, t);
  token.set(t);
}

export function clearToken() {
  localStorage.removeItem(tokenKey);
  token.set(null);
}
