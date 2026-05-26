import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "@sveltejs/kit";
import { API_URL, CANONICAL_URL, INTERNAL_API_URL } from "$lib/env";
import { TOKEN_KEY, AUTH_STATE_KEY } from "$lib/utils/auth";
import { log, logException } from "$lib/utils/logger";
import { getNextPage } from "../utils";

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get("code");

  if (!code) {
    return new Response("Erreur d'authentification : paramètre code manquant", {
      status: 400,
    });
  }

  const apiBase = INTERNAL_API_URL || API_URL;
  const tokenExchangeUrl = `${apiBase}/auth/token-exchange/`;
  let response: Response;
  try {
    response = await fetch(tokenExchangeUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
      body: JSON.stringify({ code }),
    });
  } catch (err) {
    logException(err);
    return new Response(
      "Erreur d'authentification : service d'échange de token indisponible",
      {
        status: 502,
      }
    );
  }

  if (!response.ok) {
    const body = await response.text();
    log(`callback error: token-exchange returned ${response.status}`, { body });
    return new Response(
      "Erreur d'authentification : l'échange de token a échoué",
      {
        status: 502,
      }
    );
  }

  const data = await response.json();
  const token: string = data.token;
  const expiresIn: number = data.expiresIn;

  // En HTTPS seulement — les cookies Secure sont ignorés par le navigateur sur HTTP
  const secure = url.protocol === "https:";

  cookies.set(TOKEN_KEY, token, {
    path: "/",
    httpOnly: true,
    sameSite: "lax",
    secure,
    maxAge: expiresIn,
  });

  cookies.set(AUTH_STATE_KEY, "1", {
    path: "/",
    httpOnly: false,
    sameSite: "lax",
    secure,
    maxAge: expiresIn,
  });

  const next = getNextPage(url);
  return redirect(302, CANONICAL_URL + next);
};
