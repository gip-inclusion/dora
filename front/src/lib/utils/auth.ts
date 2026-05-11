import Cookies from "js-cookie";

import { writable } from "svelte/store";

import { browser } from "$app/environment";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import type { SavedSearch, ShortBookmark, ShortStructure } from "../types";
import { log, logException } from "./logger";
import { userPreferencesSet } from "./preferences";
import { invalidateServicesOptionsCache } from "$lib/cache/services-options";

export const TOKEN_KEY =
  import.meta.env.VITE_ENVIRONMENT === "production"
    ? "token"
    : `token_${import.meta.env.VITE_ENVIRONMENT}`;

// Cookie non-httponly indiquant que l'utilisateur est connecté (lisible par JS)
export const AUTH_STATE_KEY =
  import.meta.env.VITE_ENVIRONMENT === "production"
    ? "auth_state"
    : `auth_state_${import.meta.env.VITE_ENVIRONMENT}`;

export type UserMainActivity =
  | "accompagnateur"
  | "offreur"
  | "accompagnateur_offreur"
  | "autre";

export type DiscoveryMethod =
  | "bouche-a-oreille"
  | "moteurs-de-recherche"
  | "reseaux-sociaux"
  | "evenements-dora"
  | "autre";

export interface UserInfo {
  firstName: string;
  lastName: string;
  fullName: string;
  shortName: string;
  email: string;
  newsletter: boolean;
  isStaff: boolean;
  isManager: boolean;
  cguVersionsAccepted: Record<string, string>;
  departments: string[];
  bookmarks: ShortBookmark[];
  savedSearches: SavedSearch[];
  structures: ShortStructure[];
  pendingStructures: ShortStructure[];
  mainActivity: UserMainActivity;
  discoveryMethod: DiscoveryMethod;
  discoveryMethodOther: string;
}

export const userInfo = writable<UserInfo | null>(null);

export function setUserInfo(newUserInfo: UserInfo | null) {
  userInfo.set(newUserInfo);

  // Invalide le cache des servicesOptions car les informations utilisateur ont changé
  invalidateServicesOptionsCache();
}

export function getToken() {
  if (!browser) {
    return null;
  }

  return Cookies.get(TOKEN_KEY) ?? null;
}

export function setToken(newToken: string) {
  if (!browser) {
    return;
  }

  Cookies.set(TOKEN_KEY, newToken, {
    path: "/",
    sameSite: "Lax",
    secure: true,
  });
}

export function removeToken() {
  if (!browser) {
    return;
  }

  Cookies.remove(TOKEN_KEY, {
    path: "/",
    secure: true,
    domain: window.location.hostname,
  });
}

export function isAuthenticated() {
  if (!browser) return false;
  return !!Cookies.get(AUTH_STATE_KEY);
}

function getUserInfo() {
  return fetch(`${getApiURL()}/auth/user-info/`, {
    method: "GET",
    headers: { Accept: defaultAcceptHeader },
  });
}

export async function refreshUserInfo() {
  try {
    const result = await getUserInfo();
    if (result.status === 200) {
      const info = (await result.json()) as UserInfo;
      setUserInfo(info);
      userPreferencesSet([...info.structures, ...info.pendingStructures]);
    } else {
      log("Unexpected status code", { result });
    }
  } catch (err) {
    logException(err);
  }
}

export function disconnect() {
  if (browser) {
    setUserInfo(null);
    removeToken();
    try {
      localStorage.clear();
    } catch {
      // Même en cas d'accès refusé, on poursuit la déconnexion.
    }
  }
}

function migrateTokenFromLocalStorageToCookie(
  authTokenFromCookie: string | null
) {
  if (!authTokenFromCookie) {
    try {
      const lsToken = localStorage.getItem(TOKEN_KEY);
      if (lsToken) {
        setToken(lsToken);
        localStorage.removeItem(TOKEN_KEY);
        return lsToken;
      }
    } catch {
      // Certains contextes navigateur interdisent localStorage
      // (iframe sandboxée, mode privacy strict, etc.).
    }
  }

  return authTokenFromCookie;
}

export async function validateCredsAndFillUserInfo() {
  setUserInfo(null);

  const authenticated = browser && isAuthenticated();
  console.debug("[auth] isAuthenticated:", authenticated);

  if (authenticated) {
    try {
      const result = await getUserInfo();
      console.debug("[auth] user-info status:", result.status);
      if (result.status === 200) {
        const info = await result.json();
        console.debug("[auth] user-info OK:", info.email);
        setUserInfo(info);
        userPreferencesSet([...info.structures, ...info.pendingStructures]);
      } else if (result.status === 401 || result.status === 403) {
        console.debug("[auth] user-info unauthorized, disconnecting");
        disconnect();
      } else {
        log("Unexpected status code", { result });
      }
    } catch (err) {
      console.debug("[auth] user-info fetch error:", err);
      logException(err);
    }
  }
}
