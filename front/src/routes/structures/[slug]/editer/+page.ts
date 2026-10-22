import { redirect } from "@sveltejs/kit";
import { getStructuresOptions } from "#lib/requests/structures.ts";
import { capitalize } from "#lib/utils/misc.ts";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent, params }) => {
  const { structure } = await parent();
  if (!structure.canEditInformations) {
    redirect(302, `/structures/${params.slug}`);
  }
  return {
    title: `Éditer | ${capitalize(structure.name)} | DORA`,
    noIndex: true,
    structuresOptions: await getStructuresOptions(fetch),
  };
};
