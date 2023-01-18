import { getModel, getServicesOptions } from "$lib/requests/services";
import { getStructure, getStructures } from "$lib/requests/structures";
import type { ShortStructure } from "$lib/types";
import { userInfo } from "$lib/utils/auth";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const user = get(userInfo);
  const model = await getModel(params.slug);

  const servicesOptions = await getServicesOptions();

  if (!model) {
    throw error(404, "Page Not Found");
  }

  const structure = await getStructure(model.structure);
  let structures: ShortStructure[];
  if (user.isStaff) {
    structures = await getStructures();
  } else if (user) {
    structures = user.structures;
  }

  return {
    title: `Éditer | ${model.name} | ${structure.name} | DORA`,
    noIndex: true,
    model,
    servicesOptions,
    structures,
    structure,
  };
};
