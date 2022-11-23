import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import { browser } from "$app/environment";
import { CRISP_ID } from "$lib/env";
import { userInfo, validateCredsAndFillUserInfo } from "$lib/auth";

import * as Sentry from "@sentry/browser";

import { ENVIRONMENT, SENTRY_DSN } from "$lib/env";

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
  tarteaucitron.user.crispID = CRISP_ID;
}
