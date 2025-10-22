import { getModel, getServicesOptions } from "$lib/requests/services";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  const model = await getModel(params.slug);

  if (!model) {
    error(404, "Page Not Found");
  }

  return {
    title: `${model.name} | ${model.structureInfo.name} | DORA`,
    description: "model.shortDesc",
    model,
    servicesOptions: await getServicesOptions(fetch),
  };
};
