import { redirect } from "@sveltejs/kit";

import { getApiURL } from "./api";
import { logException } from "./logger";

export async function handleInboundNexusAutoLogin(url: URL, token?: string) {
  const autoLoginJwt = url.searchParams.get("auto_login");

  if (!autoLoginJwt) {
    return;
  }

  const autoLoginUrl = `${getApiURL()}/nexus/auto-login-in/`;

  url.searchParams.delete("auto_login");

  const response = await fetch(autoLoginUrl, {
    method: "POST",
    body: JSON.stringify({
      jwt: autoLoginJwt,
      next: url.toString(),
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(token && { Authorization: `Token ${token}` }),
    },
  });

  if (response.status === 204) {
    return;
  }

  if (response.ok) {
    const data = await response.json();
    if (data.redirectUrl) {
      redirect(302, data.redirectUrl);
    }
  }
}

export function generateOutboundNexusAutoLoginUrl(url: URL | string) {
  return `/nexus/auto-login/?next=${encodeURIComponent(url.toString())}`;
}

// Demande à Nexus un lien d'auto-connexion vers `nextUrl`. Renvoie `undefined`
// si l'auto-connexion n'est pas possible (destination refusée, clé absente, API
// injoignable…) : c'est à l'appelant de décider quoi faire sans elle.
export async function fetchNexusAutoLoginUrl(nextUrl: string, token: string) {
  try {
    const response = await fetch(
      new URL("/nexus/auto-login-out/", getApiURL()),
      {
        method: "POST",
        body: JSON.stringify({ nextUrl }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json; version=1.0",
          Authorization: `Token ${token}`,
        },
      }
    );

    if (response.ok) {
      return (await response.json()).redirectUrl as string | undefined;
    }
  } catch (err) {
    logException(err, "Échec de l'auto-connexion Nexus sortante");
  }

  return undefined;
}
