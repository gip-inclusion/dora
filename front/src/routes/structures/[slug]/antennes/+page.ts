import { capitalize, markdownExcerpt } from "$lib/utils/misc";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { structure } = await parent();
  return {
    title: `Antennes | ${capitalize(structure.name)} | DORA`,
    description: markdownExcerpt(structure.fullDesc),
  };
};
