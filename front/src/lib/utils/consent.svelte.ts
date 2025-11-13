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

type ConsentConfigKey = ConsentKey | "required";
interface ConsentConfig {
  consentKey: ConsentConfigKey;
  title: string;
  description: string;
  cookies?: Array<{ title: string; description: string; link: string }>;
}

export const CONSENT_CONFIG: Record<string, ConsentConfig> = {
  required: {
    consentKey: "required",
    title: "Cookies obligatoires",
    description:
      "Ce site utilise des cookies nécessaires à son bon fonctionnement qui ne peuvent pas être désactivés. Ils incluent les cookies de session pour l'authentification et la gestion de votre consentement aux cookies.",
  },
  audience: {
    consentKey: "matomo",
    title: "Mesure d'audience",
    description:
      "Nous utilisons Matomo pour mesurer l'audience de notre site et améliorer son contenu. Vos données restent sur nos serveurs et ne sont jamais partagées avec des tiers. Ces cookies peuvent être supprimés automatiquement si vous retirez votre consentement.",
    cookies: [
      {
        title: "Matomo",
        description:
          "Matomo est un outil de mesure d'audience respectueux de la vie privée. Il peut déposer jusqu'à 7 cookies sur votre navigateur pour suivre votre navigation et nous aider à améliorer le site. Ces cookies sont stockés sur notre domaine et peuvent être supprimés à tout moment.",
        link: "https://matomo.org/faq/general/faq_146/",
      },
    ],
  },
  support: {
    consentKey: "crisp",
    title: "Support et assistance utilisateur",
    description:
      "Nous utilisons Crisp pour vous proposer un chat de support en direct. Ces cookies proviennent de notre site d'aide (aide.dora.inclusion.beta.gouv.fr) et peuvent être supprimés si vous retirez votre consentement.",
    cookies: [
      {
        title: "Crisp",
        description:
          "Crisp est un outil de chat qui nous permet de vous proposer une assistance en direct. Il peut déposer jusqu'à 5 cookies sur votre navigateur. Ces cookies proviennent de notre domaine beta.gouv.fr.",
        link: "https://crisp.chat/fr/privacy/",
      },
    ],
  },
  search: {
    consentKey: "googleCSE",
    title: "Fonctionnalité de recherche",
    description:
      "Nous utilisons Google Programmable Search Engine (CSE) pour la recherche sur notre site. Important : Les cookies Google sont stockés sur le domaine google.com. Le refus de consentement empêche le chargement de nouveaux cookies, mais ne peut pas supprimer les cookies Google existants. Pour les supprimer, utilisez les paramètres de votre navigateur. La désactivation de cette fonctionnalité peut altérer ou désactiver la recherche sur Dora.",
    cookies: [
      {
        title: "Google CSE",
        description:
          "Google Programmable Search Engine permet d'effectuer des recherches sur notre site. Limitation technique : Les cookies Google sont déposés sur le domaine google.com et ne peuvent pas être supprimés automatiquement par notre site. Le refus de consentement empêchera le chargement de la fonctionnalité de recherche et donc de nouveaux cookies Google.",
        link: "https://policies.google.com/technologies/cookies?hl=fr-fr",
      },
    ],
  },
} as const;

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
    (window as any)._paq.push(["forgetUserOptOut", false]);
  } else {
    (window as any)._paq.push(["optUserOut"]);
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
  return !hasValidConsent(consent);
}

export const cookieBannerState = $state({
  showBanner: browser ? shouldShowCookieBanner() : false,
  showDetails: false,
});

export function showCookieBanner() {
  cookieBannerState.showBanner = true;
  cookieBannerState.showDetails = !shouldShowCookieBanner();
}

export function hideCookieBanner() {
  cookieBannerState.showBanner = false;
}

export function handleBackClick() {
  if (shouldShowCookieBanner()) {
    cookieBannerState.showDetails = false;
  } else {
    hideCookieBanner();
  }
}

export function enforceCrispConsent() {
  if (!consent.consentChoices.crisp) {
    deleteCrispCookie();
  }
}
