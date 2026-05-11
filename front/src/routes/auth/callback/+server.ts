import { redirect } from "@sveltejs/kit";
import type { RequestHandler } from "@sveltejs/kit";
import { API_URL, CANONICAL_URL, INTERNAL_API_URL } from "$lib/env";
import { TOKEN_KEY, AUTH_STATE_KEY } from "$lib/utils/auth";

// 12 heures — doit correspondre à SESSION_COOKIE_AGE côté backend
const SESSION_COOKIE_AGE = 60 * 60 * 12;

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get("code");

  if (!code) {
    return new Response("callback error: no code in URL", { status: 400 });
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
    return new Response(
      `callback error: fetch to ${tokenExchangeUrl} failed — ${err}`,
      { status: 502 }
    );
  }

  if (!response.ok) {
    const body = await response.text();
    return new Response(
      `callback error: token-exchange returned ${response.status}\nURL: ${tokenExchangeUrl}\nBody: ${body}`,
      { status: 502 }
    );
  }

  const data = await response.json();
  const token: string = data.token;

  // En HTTPS seulement — les cookies Secure sont ignorés par le navigateur sur HTTP
  const secure = url.protocol === "https:";

  cookies.set(TOKEN_KEY, token, {
    path: "/",
    httpOnly: true,
    sameSite: "lax",
    secure,
    maxAge: SESSION_COOKIE_AGE,
  });

  cookies.set(AUTH_STATE_KEY, "1", {
    path: "/",
    httpOnly: false,
    sameSite: "lax",
    secure,
    maxAge: SESSION_COOKIE_AGE,
  });

  const next = url.searchParams.get("next") ?? "/";
  redirect(302, CANONICAL_URL + next);
};
