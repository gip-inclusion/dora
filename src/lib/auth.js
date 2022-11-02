import { get, writable } from "svelte/store";
import { browser } from "$app/env";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api.js";
import { log, logException } from "./logger";
import { userPreferencesSet } from "./preferences";

const tokenKey = "token";

/**
 * @typedef { import("svelte/store").Writable } Writable
 */

export const token = writable(null);
/** @type {Writable<{firstName: string, lastName: string, fullName: string, shortName: string, email: string, phoneNumber: string, newsletter: boolean,
            isStaff: boolean, isBizdev: boolean} | null>} */
export const userInfo = writable(null);

export function setToken(t) {
  token.set(t);
  localStorage.setItem(tokenKey, t);
}

async function getUserInfo(authToken) {
  return await fetch(`${getApiURL()}/auth/user-info/`, {
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
      const info = await result.json();
      userInfo.set(info);
      userPreferencesSet([...info.structures, info.pendingStructures]);
    } else {
      log("Unexpected status code", { result });
    }
  } catch (err) {
    logException(err);
  }
}

export function deleteCookies() {
  const cookies = document.cookie.split(";").reduce((acc, cookie) => {
    const [name] = cookie.split("=").map((c) => c.trim());
    acc.push(name);

    return acc;
  }, []);

  const cookieNames = Object.keys(tarteaucitron.services).reduce(
    (acc, name) => {
      acc.push(...tarteaucitron.services[name].cookies);

      return acc;
    },
    ["tarteaucitron"]
  );

  cookieNames.forEach((n) => {
    const name = cookies.find((c) => c.includes(n));

    document.cookie = `${name}=; Max-Age=0; path=/; domain=${location.hostname}`;
  });
}

export function disconnect() {
  token.set(null);
  userInfo.set(null);
  localStorage.clear();
  deleteCookies();
}

export async function validateCredsAndFillUserInfo() {
  token.set(null);
  userInfo.set(null);

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
          userInfo.set(info);
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
