import { CANONICAL_URL } from "$lib/env";
import { defaultAcceptHeader, getApiURL } from "$lib/utils/api";
import { userInfo } from "$lib/utils/auth";
import { redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async () => {
  const user = get(userInfo);

  const targetUrl = `${getApiURL()}/inclusion-connect-get-update-info/`;
  const result = await fetch(targetUrl, {
    method: "POST",
    headers: {
      Accept: defaultAcceptHeader,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      // On redirige l'utilisateur vers la page de connexion Inclusion Connect
      // pour mettre à jour les informations de l'utilisateur

      // eslint-disable-next-line camelcase
      referrer_uri: `${CANONICAL_URL}/auth/ic-connect?force_login=1&next=${encodeURIComponent(
        "/mon-compte"
      )}`,
      loginHint: user?.email,
    }),
  });

  if (result.ok) {
    const { url: icUrl } = await result.json();
    throw redirect(302, icUrl);
  }
};
