import type { PageLoad } from "../../../../../.svelte-kit/types/src/routes/(modeles-services)/services/[slug]/$types";
import { handleEmploisOrientation } from "$lib/utils/nexus";

export const load: PageLoad = async ({ url, params }) => {
  if (url.searchParams.has("op")) {
    await handleEmploisOrientation({
      serviceSlug: params.slug,
      opJwt: url.searchParams.get("op")!,
    });
  }
};
