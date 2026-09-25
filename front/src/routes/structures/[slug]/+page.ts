import { getStructuresOptions } from "$lib/requests/structures";
import { capitalize, markdownExcerpt } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent }) => {
  const { structure, members, putativeMembers } = await parent();

  return {
    title: `${capitalize(structure.name)} | DORA`,
    description: markdownExcerpt(structure.fullDesc),
    structuresOptions: await getStructuresOptions(fetch),
    members,
    putativeMembers,
  };
};
