import { browser } from "$app/environment";
import { CRISP_ID, ENVIRONMENT } from "$lib/env";
import { userInfo, validateCredsAndFillUserInfo } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { LayoutLoad } from "./$types";

// No SSR for testing => we can't intercept request server side
export const ssr = ENVIRONMENT === "testing" ? false : undefined;
export const prerender = false;
export const load: LayoutLoad = async ({ url }) => {
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
};

if (browser) {
  window.tarteaucitron.user.crispID = CRISP_ID;
}
