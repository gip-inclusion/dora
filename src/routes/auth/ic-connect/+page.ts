import { token } from "$lib/auth";
import { CANONICAL_URL } from "$lib/env";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getNextPage } from "../utils";

export const ssr = false;

export async function load({ url, fetch, parent }) {
  await parent();

  const nextPage = getNextPage(url);
  // Si on a déjà un token, on redirige directement sur la destination
  if (get(token)) {
    throw redirect(302, nextPage);
  }

  const targetUrl = `${getApiURL()}/inclusion-connect-get-login-info/`;
  const result = await fetch(targetUrl, {
    method: "POST",
    headers: {
      Accept: defaultAcceptHeader,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      redirect_uri: `${CANONICAL_URL}/auth/ic-callback?next=${encodeURIComponent(
        nextPage
      )}`,
      loginHint: url.searchParams.get("login_hint"),
    }),
  });

  if (result.ok) {
    const { url: icUrl, state } = await result.json();
    window.localStorage.setItem("oidcState", state);

    throw redirect(302, icUrl);
  }
}
