import { writable } from "svelte/store";
import { browser } from "$app/env";
import { getApiURL, defaultAcceptHeader } from "$lib/utils/api.js";
import { log, logException } from "./logger";

const tokenKey = "token";

/**
 * @typedef { import("svelte/store").Writable } Writable
 */

export const token = writable(null);
/** @type {Writable<{firstName: string, lastName: string, fullName: string, shortName: string, email: string, isStaff: boolean} | null>} */
export const userInfo = writable(null);

// Rules for auto generation by password managers
// https://developer.apple.com/password-rules/
// https://support.1password.com/compatible-website-design/
// - between 9 and 129 chars
// - not only numbers
export const passwordRules =
  "minlength: 9; maxlength: 128; required: upper,lower,special; allowed: unicode;";

export function setToken(t) {
  token.set(t);
  localStorage.setItem(tokenKey, t);
}

export function clearToken() {
  token.set(null);
  localStorage.removeItem(tokenKey);
}

export function clearUserInfo() {
  userInfo.set(null);
}

export async function getUserInfo() {
  token.set(null);
  userInfo.set(null);
  if (browser) {
    const lsToken = localStorage.getItem(tokenKey);
    if (lsToken) {
      // Check if the token is still valid
      const url = `${getApiURL()}/auth/user-info/`;
      try {
        const result = await fetch(url, {
          method: "POST",
          headers: {
            Accept: defaultAcceptHeader,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ key: lsToken }),
        });
        if (result.status === 200) {
          token.set(lsToken);
          userInfo.set(await result.json());
        } else if (result.status === 404) {
          // The token is invalid, clear localStorage
          clearToken();
          clearUserInfo();
        } else {
          log("Unexpected status code", { result });
        }
      } catch (err) {
        logException(err);
      }
    }
  }
}
