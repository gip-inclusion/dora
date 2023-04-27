import { CANONICAL_URL } from "$lib/env";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import { getNextPage } from "../utils";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ url, parent }) => {
  await parent();

  const forceLogin: boolean =
    url.searchParams.get("force_login") === "1" || false;

  const nextPage = getNextPage(url);
  // Si on a déjà un token et qu'on ne force pas le login, on redirige directement sur la destination
  if (get(token) && !forceLogin) {
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
      // eslint-disable-next-line camelcase
      redirect_uri: `${CANONICAL_URL}/auth/ic-callback?next=${encodeURIComponent(
        nextPage
      )}`,
      loginHint: url.searchParams.get("login_hint") || undefined,
    }),
  });

  if (result.ok) {
    const { url: icUrl, state } = await result.json();
    window.localStorage.setItem("oidcState", state);

    throw redirect(302, icUrl);
  }
};
