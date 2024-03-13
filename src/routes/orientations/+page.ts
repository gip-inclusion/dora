import type { PageLoad } from "./$types";
import { getOrientation } from "$lib/utils/orientation";
import { error } from "@sveltejs/kit";
import type { Orientation } from "$lib/types";

export const ssr = false;

export const load: PageLoad = async ({ url }) => {
  const token = url.searchParams.get("token");
  if (!token) {
    error(401, "Accès refusé");
  }

  const orientation = await getOrientation(token);
  if (!orientation) {
    error(404, "Page Not Found");
  }

  return {
    title: `Demande d’orientation ${orientation.id}| DORA`,
    noIndex: true,
    orientation: orientation as Orientation,
  };
};
