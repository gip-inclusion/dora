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

export function isAuthenticated() {
  if (!browser) {
    return false;
  }
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

export async function disconnect(): Promise<void> {
  if (browser) {
    try {
      await fetch("/auth/logout", { method: "POST" });
    } catch (err) {
      logException(err);
      return;
    }
    setUserInfo(null);
    try {
      localStorage.clear();
    } catch (err) {
      logException(err);
    }
  }
}

export async function validateCredsAndFillUserInfo() {
  setUserInfo(null);

  const authenticated = browser && isAuthenticated();

  if (!authenticated) {
    return;
  }

  try {
    const result = await getUserInfo();
    if (result.status === 200) {
      const info = await result.json();
      setUserInfo(info);
      userPreferencesSet([...info.structures, ...info.pendingStructures]);
    } else if (result.status === 401 || result.status === 403) {
      await disconnect();
    } else {
      log("Unexpected status code", { result });
    }
  } catch (err) {
    logException(err);
  }
}
