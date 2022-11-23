import { redirect, error } from "@sveltejs/kit";
import { browser } from "$app/environment";
import { get } from "svelte/store";

import { getModel, getService, getServicesOptions } from "$lib/services";
import { token } from "$lib/auth";

export async function load({ url, params }) {
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
    servicesOptions: await getServicesOptions({ model }),
  };
}
