import { getStructuresOptions } from "$lib/structures";
import { capitalize } from "$lib/utils";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { structure } = await parent();

  return {
    title: `Éditer | ${capitalize(structure.name)} | DORA`,
    noIndex: true,
    structuresOptions: await getStructuresOptions(),
  };
};
