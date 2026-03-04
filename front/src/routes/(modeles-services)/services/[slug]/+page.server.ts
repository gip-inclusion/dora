import { redirect } from "@sveltejs/kit";

import { getApiURL } from "$lib/utils/api";

import type { PageServerLoad } from "./$types";
import { handleEmploisOrientation } from "$lib/requests/emplois-orientation";

export const load: PageServerLoad = async ({ url, params, cookies }) => {
  const opJwt = url.searchParams.get("op");
  const alreadyProcessed = url.searchParams.has("user_structure_slug");

  if (!opJwt || alreadyProcessed) {
    return;
  }

  const token = cookies.get("token");

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
