import Cookies from "js-cookie";

import { browser } from "$app/environment";

export const CONSENT_COOKIE_NAME = "cookie_consent";

export function clearConsentCookie() {
  if (!browser) {
    return;
  }

  Cookies.remove(CONSENT_COOKIE_NAME, {
    path: "/",
    sameSite: "Lax",
    secure: true,
  });
}

export function getCookie(name: string) {
  if (!browser) {
    return undefined;
  }

  return Cookies.get(name);
}

function deleteCookieByPrefix(prefix: string, domain: string) {
  if (!browser) {
    return;
  }

  // js-cookie ne propose pas de méthode pour lister tous les cookies,
  // donc nous utilisons document.cookie pour itérer sur les cookies
  document.cookie.split(";").forEach((cookie) => {
    const cookieName = cookie.split("=")[0].trim();
    if (cookieName.startsWith(prefix)) {
      Cookies.remove(cookieName, {
        path: "/",
        domain: domain,
      });
    }
  });
}

export function deleteMatomoCookies() {
  deleteCookieByPrefix("_pk_", "dora.inclusion.gouv.fr");
}

export function deleteCrispCookie() {
  deleteCookieByPrefix("crisp-client", ".beta.gouv.fr");
}
