import { getStructuresOptions } from "$lib/structures";

export async function load({ parent }) {
  await parent();

  return {
    structuresOptions: await getStructuresOptions(),
  };
}
