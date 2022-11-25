import { setToken, validateCredsAndFillUserInfo } from "$lib/auth";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { redirect } from "@sveltejs/kit";
import { getNextPage } from "../_utils";
export const ssr = false;

export async function load({ url, fetch, parent }) {
  await parent();

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

    throw redirect(302, nextPage);
  }
  // TODO return error
}
