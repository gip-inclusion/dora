import { token, userInfo } from "$lib/utils/auth";
import { error, redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { LayoutLoad } from "./$types";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: LayoutLoad = async ({ url, parent }) => {
  await parent();

  const myToken = get(token);
  if (!myToken) {
    throw redirect(
      302,
      `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
    );
  }

  const user = get(userInfo);

  if (!user?.isStaff && !(user?.isManager && user?.departments?.length)) {
    throw error(403, "Accès réservé");
  }

  return {};
};
