import { getStructureAdmin } from "$lib/admin";
import { error } from "@sveltejs/kit";

import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const structure = await getStructureAdmin(params.slug);
  if (!structure) {
    throw error(404, "Page Not Found");
  }

  return {
    structure,
  };
};
