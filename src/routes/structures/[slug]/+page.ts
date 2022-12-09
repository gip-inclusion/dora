import { getStructuresOptions } from "$lib/structures";
import { capitalize } from "$lib/utils";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { structure } = await parent();
  return {
    title: `${capitalize(structure.name)} | DORA`,
    description: structure.shortDesc,
    structuresOptions: await getStructuresOptions(),
  };
};
