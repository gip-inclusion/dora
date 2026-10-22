import { getStructuresOptions } from "#lib/requests/structures.js";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  return {
    title: "Créer une structure | Administration | DORA",
    noIndex: true,
    structuresOptions: await getStructuresOptions(fetch),
  };
};
