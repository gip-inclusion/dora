import { error } from "@sveltejs/kit";
import { browser } from "$app/env";
import { getModel, getServicesOptions } from "$lib/services";

export async function load({ params }) {
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
