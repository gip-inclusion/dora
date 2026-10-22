import { getStructuresOptions } from "#lib/requests/structures.ts";
import { capitalize } from "#lib/utils/misc.ts";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent }) => {
  const { structure, members, putativeMembers } = await parent();

  return {
    title: `${capitalize(structure.name)} | DORA`,
    description: structure.shortDescription,
    structuresOptions: await getStructuresOptions(fetch),
    members,
    putativeMembers,
  };
};
