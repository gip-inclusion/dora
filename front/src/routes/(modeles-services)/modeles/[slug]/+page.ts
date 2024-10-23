import { browser } from "$app/environment";
import { getModel, getServicesOptions } from "$lib/requests/services";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const model = await getModel(params.slug);

  // on ne retourne une 404 que sur le client
  if (!model && !browser) {
    return {};
  }

  if (!model) {
    error(404, "Page Not Found");
  }

  return {
    title: `${model.name} | ${model.structureInfo.name} | DORA`,
    description: "model.shortDesc",
    model,
    servicesOptions: await getServicesOptions(),
  };
};
