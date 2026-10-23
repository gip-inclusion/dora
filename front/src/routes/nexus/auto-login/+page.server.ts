import { error, redirect } from "@sveltejs/kit";
import type { RequestEvent } from "@sveltejs/kit";
import { INCLUSION_PLATFORM_URL } from "#lib/env.ts";
import { TOKEN_KEY } from "#lib/utils/auth.ts";
import { fetchNexusAutoLoginUrl } from "#lib/utils/nexus.ts";

// Seule destination vers laquelle on accepte de rediriger sans auto-connexion.
// Le contrôle est indispensable : sur ce chemin, l'URL demandée n'est jamais
// soumise au back (qui la valide contre `NEXUS_ALLOWED_REDIRECT_HOSTS`), donc
// sans autorisation explicite la route serait une redirection ouverte.
const FALLBACK_ALLOWED_ORIGIN = new URL(INCLUSION_PLATFORM_URL).origin;

function hasAllowedOrigin(nextUrl: string) {
  let origin: string;
  try {
    origin = new URL(nextUrl).origin;
  } catch {
    return false;
  }

  return origin === FALLBACK_ALLOWED_ORIGIN;
}

export const load = async ({ cookies, url }: RequestEvent) => {
  const token = cookies.get(TOKEN_KEY) ?? null;

  const nextUrl = url.searchParams.get("next");

  if (!nextUrl) {
    error(404, "Page Not Found");
  }

  // l'auto-connexion est un confort : si elle n'aboutit pas, on envoie tout de
  // même l'utilisateur à destination, qui l'invitera à se connecter
  const fallback = hasAllowedOrigin(nextUrl) ? nextUrl : null;

  if (!token) {
    if (fallback) {
      redirect(302, fallback);
    }
    error(404, "Page Not Found");
  }

  const autoLoginRedirectUrl = await fetchNexusAutoLoginUrl(nextUrl, token);

  if (autoLoginRedirectUrl) {
    redirect(302, autoLoginRedirectUrl);
  }

  if (fallback) {
    redirect(302, fallback);
  }

  error(404, "Page Not Found");
};
