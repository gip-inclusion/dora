import { redirect } from "@sveltejs/kit";
export const ssr = false;

import { get } from "svelte/store";
import { token } from "$lib/auth";
import { getNextPage } from "../_utils";

export async function load({ url, parent }) {
  await parent();

  const nextPage = getNextPage(url);
  // Si on a déjà un token, on redirige directement sur la destination
  if (get(token)) {
    throw redirect(302, nextPage);
  }
  return {};
}
