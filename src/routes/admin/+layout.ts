import { redirect, error } from "@sveltejs/kit";
import { token, userInfo } from "$lib/auth";
import { get } from "svelte/store";

export async function load({ url }) {
  const myToken = get(token);
  if (!myToken) {
    throw redirect(
      302,
      `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
    );
  }

  const user = get(userInfo);

  if (!user?.isStaff) {
    throw error(403, "Accès réservé");
  }

  return {};
}
