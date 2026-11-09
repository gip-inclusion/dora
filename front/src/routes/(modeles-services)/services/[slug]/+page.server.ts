import { redirect } from "@sveltejs/kit";

import type { PageServerLoad } from "./$types";
import { handleEmploisOrientation } from "#lib/requests/emplois-orientation.ts";
import { ORIENTATION_JWT_QUERY_PARAM } from "#lib/consts.ts";
import { TOKEN_KEY } from "#lib/utils/auth.ts";
import { transferUrlParams } from "#lib/utils/misc.ts";

export const load: PageServerLoad = async ({ url, params, cookies }) => {
  const opJwt = url.searchParams.get(ORIENTATION_JWT_QUERY_PARAM);
  const alreadyProcessed = url.searchParams.has("user_structure_slug");

  if (!opJwt || alreadyProcessed) {
    return;
  }

  const token = cookies.get(TOKEN_KEY);

  const response = await handleEmploisOrientation({
    serviceSlug: params.slug,
    opJwt,
    token,
  });

  if (response.ok) {
    const data = await response.json();
    if (data.nextUrl) {
      // Le back construit `nextUrl` à partir de son `FRONTEND_URL` : on n'en
      // garde que le chemin, pour rester sur l'origine courante même quand
      // celle-ci diffère (front local branché sur l'API de staging, review app)
      const nextUrl = new URL(
        transferUrlParams({
          targetUrl: data.nextUrl,
          sourceUrl: url,
          exclude: [ORIENTATION_JWT_QUERY_PARAM],
        })
      );
      redirect(302, `${nextUrl.pathname}${nextUrl.search}`);
    }
  }
};
