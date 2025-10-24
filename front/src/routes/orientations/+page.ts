import type { PageLoad } from "./$types";
import { getOrientation } from "$lib/utils/orientation";
import { error } from "@sveltejs/kit";
import type { Orientation } from "$lib/types";
export const ssr = false;

export const load: PageLoad = async ({ fetch, parent, url }) => {
  await parent();
  const queryId = url.searchParams.get("token");
  const queryHash = url.searchParams.get("h");

  if (!queryHash || !queryId) {
    error(401, "Accès refusé");
  }

  return getOrientation(queryId, queryHash, fetch).then((response) => {
    if (response.status === 404) {
      error(404, "Non trouvé");
    }
    const orientation = response.ok ? (response.data as Orientation) : null;
    return {
      title: orientation
        ? `Demande d’orientation ${orientation.id}| DORA`
        : "Demande d’orientation DORA",
      orientation: orientation,
      queryHash: queryHash,
      queryId: queryId,
      askForNewLink: !response.ok,
      noIndex: true,
    };
  });
};
