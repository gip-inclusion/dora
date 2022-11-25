import { browser } from "$app/environment";
import { userInfo, validateCredsAndFillUserInfo } from "$lib/auth";
import { CRISP_ID, ENVIRONMENT, SENTRY_DSN } from "$lib/env";
import * as Sentry from "@sentry/browser";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";

// No SSR for testing => we can't intercept request server side
export const ssr = ENVIRONMENT === "testing" ? false : undefined;

if (ENVIRONMENT !== "local") {
  Sentry.init({
    dsn: SENTRY_DSN,
    environment: ENVIRONMENT,
    tracesSampleRate: 0,
  });
}

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
