import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";

// pages authentifiées sur lesquelles la première requête non authentifiée n'a pas de sens
export const ssr = false;

export const load: PageLoad = async ({ parent }) => {
  await parent();

  return {
    title: "Créer une structure | DORA",
    noIndex: true,
    structuresOptions: await getStructuresOptions(),
  };
};
