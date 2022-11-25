import { token } from "$lib/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getNextPage } from "../utils";
export const ssr = false;

export async function load({ url, parent }) {
  await parent();

  const nextPage = getNextPage(url);
  // Si on a déjà un token, on redirige directement sur la destination
  if (get(token)) {
    throw redirect(302, nextPage);
  }
  return {};
}
