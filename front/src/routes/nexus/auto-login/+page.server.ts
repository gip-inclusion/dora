import { getApiURL } from "$lib/utils/api";
import { error, redirect } from "@sveltejs/kit";
import type { RequestEvent } from "@sveltejs/kit";
import { INCLUSION_PLATFORM_URL } from "$lib/env";
import { TOKEN_KEY } from "$lib/utils/auth";

// Seule destination vers laquelle on accepte de rediriger sans auto-connexion.
// Le contrôle est indispensable : sur ce chemin, l'URL demandée n'est jamais
// soumise au back (qui la valide contre `NEXUS_ALLOWED_REDIRECT_HOSTS`), donc
// sans autorisation explicite la route serait une redirection ouverte.
const FALLBACK_ALLOWED_ORIGIN = new URL(INCLUSION_PLATFORM_URL).origin;

// Renvoie `nextUrl` si on a le droit de s'y rendre sans auto-connexion, sinon `null`
function getAllowedFallbackUrl(nextUrl: string) {
  let origin: string;
  try {
    origin = new URL(nextUrl).origin;
  } catch {
    return null;
  }

  return origin === FALLBACK_ALLOWED_ORIGIN ? nextUrl : null;
}

export const load = async ({ cookies, url }: RequestEvent) => {
  const token = cookies.get(TOKEN_KEY) ?? null;

  const nextUrl = url.searchParams.get("next");

  if (!nextUrl) {
    error(404, "Page Not Found");
  }

  // l'auto-connexion est un confort : si elle n'aboutit pas, on envoie tout de
  // même l'utilisateur à destination, qui l'invitera à se connecter
  const fallback = getAllowedFallbackUrl(nextUrl);

  if (!token) {
    if (fallback) {
      redirect(302, fallback);
    }
    error(404, "Page Not Found");
  }

  const autoLoginUrl = new URL("/nexus/auto-login-out/", getApiURL());

  const response = await fetch(autoLoginUrl, {
    method: "POST",
    body: JSON.stringify({
      nextUrl,
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      Authorization: `Token ${token}`,
    },
  });

  if (response.ok) {
    const data = await response.json();
    if (data.redirectUrl) {
      redirect(302, data.redirectUrl);
    }
  }

  if (fallback) {
    redirect(302, fallback);
  }

  error(404, "Page Not Found");
};
