import { browser } from "$app/environment";
import { log } from "$lib/utils/logger";
import {
  clearConsentCookie,
  CONSENT_COOKIE_NAME,
  deleteCrispCookie,
  deleteMatomoCookies,
  getCookie,
} from "$lib/utils/cookie";
import { sendConsentToAPI } from "$lib/requests/consent";

export const CONSENT_VERSION = "1.0";
const CONSENT_EXPIRY_MONTHS = 13;

const CONSENT_KEYS = ["matomo", "googleCSE", "crisp"] as const;

export type ConsentKey = (typeof CONSENT_KEYS)[number];

export type ConsentChoices = Record<ConsentKey, boolean>;

export interface Consent {
  version: string;
  consentChoices: ConsentChoices;
  timestamp: string;
}

const defaultConsent: Consent = {
  version: CONSENT_VERSION,
  consentChoices: {
    matomo: true,
    googleCSE: true,
    crisp: true,
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

function loadConsent() {
  if (!browser) {
    return defaultConsent;
  }

  const cookieConsent = getCookie(CONSENT_COOKIE_NAME);
  if (cookieConsent) {
    try {
      const parsedConsent = JSON.parse(cookieConsent);

      if (!hasValidConsent(parsedConsent)) {
        clearConsentCookie();
        return defaultConsent;
      }

      return parsedConsent as Consent;
    } catch (error) {
      log("Le contenu du cookie de consentement n'a pas pu être parsé", error);
    }
  }

  return defaultConsent;
}

export const consent: Consent = $state(loadConsent());

function hasConsentChanged(current: Consent, updates: ConsentChoices) {
  return (
    !current.timestamp ||
    CONSENT_KEYS.some(
      (key) =>
        Object.hasOwn(updates, key) &&
        updates[key] !== current.consentChoices[key]
    )
  );
}

function enforceMatomoConsent(hasMatomoConsent: boolean) {
  if (hasMatomoConsent) {
    (window as any)._paq.push(["optUserOut"]);
  } else {
    (window as any)._paq.push(["forgetUserOptOut", false]);
    deleteMatomoCookies();
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

  if (consent.consentChoices.matomo !== consentChoices.matomo) {
    enforceMatomoConsent(consentChoices.matomo);
  }

  //On ne peut pas exporter un $state déclaré avec un let donc il faut modifier les propriétés individuellement
  consent.consentChoices = consentChoices;
  consent.timestamp = now;
}

export function shouldShowCookieBanner() {
  // return !hasValidConsent(consent);
  return true;
}

export function enforceCrispConsent() {
  if (!consent.consentChoices.crisp) {
    deleteCrispCookie();
  }
}

export const CONSENT_CONFIG = {
  required: {
    consentKey: "required",
    title: "Cookies obligatoires",
    description:
      "Ce site utilise des cookies nécessaires à son bon fonctionnement qui ne peuvent pas être désactivés.",
  },
  audience: {
    consentKey: "matomo",
    title: "Mesure d'audience",
    description:
      "Nous utilisons des cookies pour mesurer l’audience de notre site et améliorer son contenu.",
    cookies: [
      {
        title: "Matomo",
        description:
          "Matomo est un outil de mesure d'audience qui nous permet de suivre les visites de notre site et d'améliorer son contenu. Il peut déposer 7 cookies sur votre navigateur.\n" +
          "Voir le site officiel",
      },
    ],
  },
  support: {
    consentKey: "crisp",
    title: "Support et assistance utilisateur",
    description:
      "Nous utilisons les cookies pour vous proposer la fonctionnalité de contact par chat avec le support de Dora",
    cookies: [
      {
        title: "Crisp",
        description:
          "Crisp est un outil de chat qui nous permet de vous proposer la fonctionnalité de contact par chat avec le support d'Immersion Facilitée. Il peut déposer 5 cookies sur votre navigateur.",
      },
    ],
  },
  search: {
    consentKey: "googleCSE",
    title: "Fonctionnalité de recherche",
    description:
      "Nous utilisons Google Programmable Search Engine (CSE) pour vous permettre d’effectuer des recherches sur notre site à l’aide de la technologie Google.\n" +
      "La désactivation de cette fonctionnalité peut altérer ou désactiver la recherche sur Dora.",
    cookies: [
      {
        title: "Google CSE",
        description:
          "Google CSE est un outil de recherche qui nous permet de vous proposer la fonctionnalité de contact par chat avec le support d'Immersion Facilitée. Il peut déposer 5 cookies sur votre navigateur.",
      },
    ],
  },
};
