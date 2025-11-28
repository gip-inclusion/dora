import { get } from "svelte/store";
import { token } from "./auth";
import { getApiURL } from "./api";
import { redirect } from "@sveltejs/kit";
import { disconnect } from "./auth";

export async function handleNexusAutoLogin(url: URL) {
  const autoLoginJwt = url.searchParams.get("auto_login");

  if (!autoLoginJwt) {
    return;
  }

  const autoLoginUrl = new URL("/nexus/auto-login-in/", getApiURL());

  url.searchParams.delete("auto_login");

  // Reconstruire la chaîne de recherche pour s'assurer qu'elle est à jour
  const updatedSearch = url.searchParams.toString();
  const nextUrl = url.pathname + (updatedSearch ? `?${updatedSearch}` : "");

  const response = await fetch(autoLoginUrl, {
    method: "POST",
    body: JSON.stringify({
      jwt: autoLoginJwt,
      next: nextUrl,
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(get(token) && { Authorization: `Token ${get(token)}` }),
    },
  });

  if (response.status === 204) {
    return;
  }

  if (response.ok) {
    const data = await response.json();
    if (data.redirectUrl) {
      disconnect();
      redirect(302, data.redirectUrl);
    }
  }
}
