import { redirect } from "@sveltejs/kit";

import type { PageServerLoad } from "./$types";
import { handleEmploisOrientation } from "$lib/requests/emplois-orientation";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";
import { TOKEN_KEY } from "$lib/utils/auth";

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
      redirect(302, data.nextUrl);
    }
  }
};
