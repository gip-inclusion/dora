import { browser } from "$app/environment";
import { token } from "$lib/auth";
import { getModel, getService, getServicesOptions } from "$lib/services";
import { getStructure } from "$lib/structures";
import { error, redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ url, params, parent }) => {
  await parent();

  const service = await getService(params.slug);
  // si le service est en brouillon il faut un token pour y accéder
  // on renvoie donc un objet vide côté serveur
  if (!service) {
    if (!browser) {
      return {
        service: null,
      };
    }
    if (!get(token)) {
      throw redirect(
        302,
        `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
      );
    }
    throw error(404, "Page Not Found");
  }

  const model = service.model ? await getModel(service.model) : null;

  return {
    service,
    structure: await getStructure(service.structure),
    servicesOptions: await getServicesOptions({ model }),
  };
};
