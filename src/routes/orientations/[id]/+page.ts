import type { PageLoad } from "./$types";
import { getOrientation } from "$lib/utils/orientation";
import { error } from "@sveltejs/kit";
import type { Orientation } from "$lib/types";

export const ssr = false;

export const load: PageLoad = async ({ params }) => {
  const orientation = await getOrientation(params.id);

  if (!orientation) {
    throw error(404, "Page Not Found");
  }

  return {
    title: `Demande d’orientation ${orientation.id}| DORA`,
    noIndex: true,
    orientation: orientation as Orientation,
  };
};
