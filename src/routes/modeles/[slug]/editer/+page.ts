import { userInfo } from "$lib/auth";
import { getModel, getServicesOptions } from "$lib/services";
import { getStructure, getStructures } from "$lib/structures";
import type { ShortStructure } from "$lib/types";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const user = get(userInfo);
  const model = await getModel(params.slug);

  const servicesOptions = await getServicesOptions({ model });

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
    model,
    servicesOptions,
    structures,
    structure,
  };
};
