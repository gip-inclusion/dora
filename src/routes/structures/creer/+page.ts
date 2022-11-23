import { getStructuresOptions } from "$lib/structures";

export async function load() {
  return { structuresOptions: await getStructuresOptions() };
}
