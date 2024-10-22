import { getStructureAdmin } from "$lib/requests/admin";
import { capitalize } from "$lib/utils/misc";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const structure = await getStructureAdmin(params.slug);
  if (!structure) {
    error(404, "Page Not Found");
  }

  return {
    title: `${capitalize(structure.name)} | Administration | DORA`,
    noIndex: true,
    structure,
  };
};
