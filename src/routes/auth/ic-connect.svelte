<script context="module">
  import { CANONICAL_URL } from "$lib/env.js";
  import { token } from "$lib/auth";
  import { get } from "svelte/store";
  import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
  import { getNextPage } from "./utils.js";

  export const ssr = false;

  export async function load({ url, fetch }) {
    const nextPage = getNextPage(url);
    // Si on a déjà un token, on redirige directement sur la destination
    if (get(token)) {
      return {
        status: 302,
        redirect: nextPage,
      };
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
      let { url: icUrl, state } = await result.json();
      window.localStorage.setItem("oidcState", state);

      return {
        status: 302,
        redirect: icUrl,
      };
    }
  }
</script>
