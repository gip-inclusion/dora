<script context="module">
  export const ssr = false;

  import { setToken, validateCredsAndFillUserInfo } from "$lib/auth";
  import { getApiURL, defaultAcceptHeader } from "$lib/utils/api";
  import { getNextPage } from "./utils.js";

  export async function load({ url, fetch }) {
    const nextPage = getNextPage(url);

    const query = url.searchParams;

    // TODO: error if any of those are empty
    const code = query.get("code");
    const state = query.get("state");

    const storedState = window.localStorage.getItem("oidcState");
    window.localStorage.removeItem("oidcState");

    const targetUrl = `${getApiURL()}/inclusion-connect-authenticate/`;
    const result = await fetch(targetUrl, {
      method: "POST",
      headers: {
        Accept: defaultAcceptHeader,
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        code,
        state,
        frontendState: storedState,
      }),
    });

    let jsonResult = {};

    if (result.ok) {
      jsonResult = await result.json();
      setToken(jsonResult.token);
      await validateCredsAndFillUserInfo();

      return {
        status: 302,
        redirect: nextPage,
      };
    }
    // TODO return error
  }
</script>
