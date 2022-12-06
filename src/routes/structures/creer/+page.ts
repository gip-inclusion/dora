import { getStructuresOptions } from "$lib/structures";
import type { PageLoad } from "./$types";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ parent }) => {
  await parent();

  return { structuresOptions: await getStructuresOptions() };
};
