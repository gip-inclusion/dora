import { browser } from "$app/environment";
import { userInfo, validateCredsAndFillUserInfo } from "$lib/auth";
import { CRISP_ID } from "$lib/env";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";

export const ssr = false;

// No SSR for testing => we can't intercept request server side
// export const ssr = ENVIRONMENT === "testing" ? false : undefined;

export async function load({ url }) {
  let currentUserInfo = get(userInfo);
  if (!currentUserInfo) {
    await validateCredsAndFillUserInfo();
    currentUserInfo = get(userInfo);
  }
  if (
    currentUserInfo &&
    !(
      currentUserInfo.structures.length ||
      currentUserInfo.pendingStructures.length
    ) &&
    !url.pathname.startsWith("/auth/rattachement") &&
    !url.pathname.startsWith("/auth/invitation") &&
    !url.pathname.startsWith("/auth/deconnexion")
  ) {
    throw redirect(302, "/auth/rattachement");
  }
  return {};
}

if (browser) {
  window.tarteaucitron.user.crispID = CRISP_ID;
}
