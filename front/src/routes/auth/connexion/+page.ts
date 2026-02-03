import { redirect } from "@sveltejs/kit";

import { getToken } from "$lib/utils/auth";

import { getNextPage } from "../utils";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const nextPage = getNextPage(url);
  // Si on a déjà un token, on redirige directement sur la destination
  if (getToken()) {
    redirect(302, nextPage);
  }
  return {
    title: "Connexion / Inscription | DORA",
    noIndex: true,
  };
};
