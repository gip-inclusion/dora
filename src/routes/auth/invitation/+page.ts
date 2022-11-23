import { error } from "@sveltejs/kit";
import { getStructure } from "$lib/structures";

export async function load({ url }) {
  const structure = await getStructure(url.searchParams.get("structure"));
  let parent = null;
  if (!structure) {
    throw error(404, "Page Not Found");
  }

  if (structure.parent) {
    parent = await getStructure(structure.parent);
  }

  return { structure, parent };
}
