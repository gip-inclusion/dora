import { redirect } from "@sveltejs/kit";
import { getStructuresOptions } from "$lib/requests/structures";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent, params }) => {
  const { structure } = await parent();
  if (!structure.canEditInformations) {
    throw redirect(302, `/structures/${params.slug}`);
  }
  return {
    title: `Éditer | ${capitalize(structure.name)} | DORA`,
    noIndex: true,
    structuresOptions: await getStructuresOptions(),
  };
};
