import { getModel, getServicesOptions } from "$lib/requests/services";
import { getStructure } from "$lib/requests/structures";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  const model = await getModel(params.slug, fetch);

  const servicesOptions = await getServicesOptions(fetch);

  if (!model) {
    error(404, "Page Not Found");
  }

  const structure = await getStructure(model.structure, fetch);

  return {
    title: `Éditer | ${model.name} | ${structure.name} | DORA`,
    noIndex: true,
    model,
    servicesOptions,
    structures: [structure],
    structure,
  };
};
