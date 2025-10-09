import { browser } from "$app/environment";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { get, writable } from "svelte/store";
import type { SavedSearch, ShortBookmark, ShortStructure } from "../types";
import { log, logException } from "./logger";
import { userPreferencesSet } from "./preferences";
import { invalidateServicesOptionsCache } from "$lib/cache/services-options";

const tokenKey = "token";

export const token = writable<string | null>(null);

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

export function setToken(newToken: string) {
  token.set(newToken);
  localStorage.setItem(tokenKey, newToken);
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
    const result = await getUserInfo(get(token));
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
  token.set(null);
  setUserInfo(null);
  localStorage.clear();
}

export async function validateCredsAndFillUserInfo() {
  token.set(null);
  setUserInfo(null);

  if (browser) {
    const lsToken = localStorage.getItem(tokenKey);
    if (lsToken) {
      // Valide le token actuel et remplit les informations
      // utilisateur
      try {
        const result = await getUserInfo(lsToken);
        if (result.status === 200) {
          token.set(lsToken);
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
