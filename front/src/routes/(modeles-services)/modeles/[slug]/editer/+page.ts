import { getModel, getServicesOptions } from "$lib/requests/services";
import { getStructure } from "$lib/requests/structures";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  const model = await getModel(params.slug, fetch);

  if (!model) {
    error(404, "Page Not Found");
  }

  const [structure, servicesOptions] = await Promise.all([
    getStructure(model.structure, fetch),
    getServicesOptions(fetch),
  ]);

  return {
    title: `Éditer | ${model.name}${structure ? ` | ${structure.name}` : ""} | DORA`,
    noIndex: true,
    model,
    servicesOptions,
    structures: structure ? [structure] : [],
    structure,
  };
};
