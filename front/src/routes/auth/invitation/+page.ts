import { getStructure } from "$lib/requests/structures";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();

  const structure = await getStructure(
    url.searchParams.get("structure"),
    fetch
  );
  let structureParent = null;
  if (!structure) {
    error(404, "Page Not Found");
  }

  if (structure.parent) {
    structureParent = await getStructure(structure.parent, fetch);
  }

  return {
    title: "Invitation | DORA",
    noIndex: true,
    structure,
    parent: structureParent,
  };
};
