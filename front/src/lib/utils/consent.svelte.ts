import { browser } from "$app/environment";
import { getApiURL } from "$lib/utils/api";
import { getAnalyticsId } from "$lib/utils/stats";
import { log } from "$lib/utils/logger";

const CONSENT_COOKIE_NAME = "cookie_consent";
const CONSENT_VERSION = "1.0";
const CONSENT_EXPIRY_MONTHS = 13;

export const CONSENT_KEYS = ["matomo", "googleCSE", "crisp"] as const;

type ConsentKey = (typeof CONSENT_KEYS)[number];

export type ConsentChoices = Record<ConsentKey, boolean>;

interface Consent {
  version: string;
  consentChoices: ConsentChoices;
  timestamp: string;
}

const defaultConsent: Consent = {
  version: CONSENT_VERSION,
  consentChoices: {
    matomo: false,
    googleCSE: false,
    crisp: false,
  },
  timestamp: "",
};

function isConsentExpired(timestamp: string) {
  if (!timestamp) {
    return true;
  }

  const consentDate = new Date(timestamp);
  const expiryDate = new Date(consentDate);
  expiryDate.setMonth(expiryDate.getMonth() + CONSENT_EXPIRY_MONTHS);

  return new Date() > expiryDate;
}

function isConsentOutdated(version) {
  return version !== CONSENT_VERSION;
}

function hasValidConsent(currentConsent: Consent) {
  if (!browser) {
    return false;
  }

  return (
    currentConsent.timestamp &&
    !isConsentExpired(currentConsent.timestamp) &&
    !isConsentOutdated(currentConsent.version) &&
    CONSENT_KEYS.every((key) =>
      Object.hasOwn(currentConsent.consentChoices, key)
    )
  );
}

function clearConsent() {
  if (!browser) {
    return;
  }

  document.cookie = `${CONSENT_COOKIE_NAME}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Lax; Secure`;
}

function getCookie(name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop()?.split(";").shift();
  }

  return undefined;
}

function loadConsent() {
  if (!browser) {
    return defaultConsent;
  }

  const cookieConsent = getCookie(CONSENT_COOKIE_NAME);
  if (cookieConsent) {
    try {
      const parsedConsent = JSON.parse(cookieConsent);

      if (!hasValidConsent(parsedConsent)) {
        clearConsent();
        return defaultConsent;
      }

      return parsedConsent as Consent;
    } catch (error) {
      log("Le contenu du cookie de consentement n'a pas pu être lu", error);
    }
  }

  return defaultConsent;
}

export const consent: Consent = $state(loadConsent());

function hasConsentChanged(current: Consent, updates: ConsentChoices) {
  return CONSENT_KEYS.some(
    (key) =>
      Object.hasOwn(updates, key) &&
      updates[key] !== current.consentChoices[key]
  );
}

async function sendConsentToAPI(consentChoices: Consent["consentChoices"]) {
  try {
    await fetch(`${getApiURL()}/consent-record/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        consentChoices,
        consentVersion: CONSENT_VERSION,
        anonymousUserHash: getAnalyticsId(),
      }),
    });
  } catch (error) {
    log("Le consentement de l'utilisateur n'a pas été sauvegardé", error);
  }
}

function handleMatomoConsent(hasMatomoConsent: boolean) {
  if (hasMatomoConsent) {
    (window as any)._paq.push(["optUserOut"]);
  } else {
    (window as any)._paq.push(["forgetUserOptOut", false]);
  }
}

function persistConsent(updatedConsent: Consent) {
  const consentString = JSON.stringify(updatedConsent);

  const expiryDate = new Date();
  expiryDate.setMonth(expiryDate.getMonth() + CONSENT_EXPIRY_MONTHS);
  document.cookie = `${CONSENT_COOKIE_NAME}=${consentString}; expires=${expiryDate.toUTCString()}; path=/; SameSite=Lax; Secure`;

  sendConsentToAPI(updatedConsent.consentChoices);
}

export function setConsentChoices(consentChoices: ConsentChoices) {
  if (!browser) {
    return;
  }

  if (!hasConsentChanged(consent, consentChoices)) {
    return;
  }

  const now = new Date().toISOString();

  const updatedConsent = {
    consentChoices,
    version: CONSENT_VERSION,
    timestamp: now,
  };
  persistConsent(updatedConsent);

  handleMatomoConsent(consentChoices.matomo);

  //On ne peut pas exporter un $state déclaré avec un let donc il faut modifier les propriétés
  consent.consentChoices = consentChoices;
  consent.timestamp = now;
}

export function shouldShowBanner() {
  if (!browser) {
    return false;
  }

  if (!consent.timestamp) {
    return true;
  }

  if (isConsentExpired(consent.timestamp)) {
    return true;
  }

  if (isConsentOutdated(consent.version)) {
    return true;
  }

  return false;
}

export function enforceCrispConsent() {
  if (!browser) {
    return;
  }

  if (!consent.consentChoices.crisp) {
    document.cookie.split(";").forEach((cookie) => {
      const cookieName = cookie.split("=")[0].trim();
      if (cookieName.startsWith("crisp-client")) {
        document.cookie = `${cookieName}=;max-age=0;path=/;domain=.beta.gouv.fr`;
      }
    });
  }
}
