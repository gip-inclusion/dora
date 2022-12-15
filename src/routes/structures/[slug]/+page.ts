import { getStructuresOptions } from "$lib/requests/structures";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { structure } = await parent();
  return {
    title: `${capitalize(structure.name)} | DORA`,
    description: structure.shortDesc,
    structuresOptions: await getStructuresOptions(),
  };
};
