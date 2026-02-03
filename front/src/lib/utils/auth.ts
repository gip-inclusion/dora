import Cookies from "js-cookie";

import { writable } from "svelte/store";

import { browser } from "$app/environment";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import type { SavedSearch, ShortBookmark, ShortStructure } from "../types";
import { log, logException } from "./logger";
import { userPreferencesSet } from "./preferences";
import { invalidateServicesOptionsCache } from "$lib/cache/services-options";

const TOKEN_KEY = "token";

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

function getUserInfo(authToken) {
  return fetch(`${getApiURL()}/auth/user-info/`, {
    method: "POST",
    headers: {
      Accept: defaultAcceptHeader,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ key: authToken }),
  });
}

export async function refreshUserInfo() {
  try {
    const result = await getUserInfo(getToken());
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
    localStorage.clear();
  }
}

function migrateTokenFromLocalStorageToCookie(
  authTokenFromCookie: string | null
) {
  if (!authTokenFromCookie) {
    const lsToken = localStorage.getItem(TOKEN_KEY);
    if (lsToken) {
      setToken(lsToken);
      localStorage.removeItem(TOKEN_KEY);
      return lsToken;
    }
  }

  return authTokenFromCookie;
}

export async function validateCredsAndFillUserInfo() {
  setUserInfo(null);

  if (browser) {
    let authToken = getToken();

    authToken = migrateTokenFromLocalStorageToCookie(authToken);

    if (authToken) {
      // Valide le token actuel et remplit les informations
      // utilisateur
      try {
        const result = await getUserInfo(authToken);
        if (result.status === 200) {
          const info = await result.json();
          setUserInfo(info);
          userPreferencesSet([...info.structures, ...info.pendingStructures]);
        } else if (result.status === 404) {
          // Le token est invalide, on déconnecte l'utilisateur
          disconnect();
        } else {
          log("Unexpected status code", { result });
        }
      } catch (err) {
        logException(err);
      }
    }
  }
}
