import { getStructuresOptions } from "$lib/requests/structures";
import { capitalize } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { structure } = await parent();

  return {
    title: `Éditer | ${capitalize(structure.name)} | DORA`,
    noIndex: true,
    structuresOptions: await getStructuresOptions(),
  };
};
