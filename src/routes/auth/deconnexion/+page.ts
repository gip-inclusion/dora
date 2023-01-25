import { CANONICAL_URL } from "$lib/env";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { disconnect } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  await parent();

  const targetUrl = `${getApiURL()}/inclusion-connect-get-logout-info/`;
  const result = await fetch(targetUrl, {
    method: "POST",
    headers: {
      Accept: defaultAcceptHeader,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      // eslint-disable-next-line camelcase
      redirect_uri: CANONICAL_URL,
    }),
  });
  let jsonResult = {};

  if (result.ok) {
    jsonResult = await result.json();
    disconnect();
    throw redirect(302, jsonResult.url);
  }
  // TODO: surface error
};
