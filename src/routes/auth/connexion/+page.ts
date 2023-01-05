import { token } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getNextPage } from "../utils";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const nextPage = getNextPage(url);
  // Si on a déjà un token, on redirige directement sur la destination
  if (get(token)) {
    throw redirect(302, nextPage);
  }
  return {
    title: "Connexion / Inscription | DORA",
    noIndex: true,
  };
};
