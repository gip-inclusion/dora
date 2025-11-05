import { browser } from "$app/environment";

export const CONSENT_COOKIE_NAME = "cookie_consent";

export function clearConsentCookie() {
  if (!browser) {
    return;
  }

  document.cookie = `${CONSENT_COOKIE_NAME}=; max-age=0; path=/; SameSite=Lax; Secure`;
}

export function getCookie(name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(";").shift();
  }

  return undefined;
}

export function deleteCrispCookie() {
  if (!browser) {
    return;
  }

  document.cookie.split(";").forEach((cookie) => {
    const cookieName = cookie.split("=")[0].trim();
    if (cookieName.startsWith("crisp-client")) {
      document.cookie = `${cookieName}=; max-age=0; path=/;domain=localhost`;
    }
  });
}
