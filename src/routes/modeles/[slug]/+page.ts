import { browser } from "$app/environment";
import { getModel, getServicesOptions } from "$lib/services";
import { error } from "@sveltejs/kit";

export async function load({ params, parent }) {
  await parent();

  const model = await getModel(params.slug);

  // on ne retourne une 404 que sur le client
  if (!model && !browser) {
    return {};
  }

  if (!model) {
    throw error(404, "Page Not Found");
  }

  return {
    model,
    servicesOptions: await getServicesOptions(),
  };
}
