import { browser } from "$app/environment";
import { getService, getServicesOptions } from "$lib/requests/services";
import { getStructure } from "$lib/requests/structures";
import { token } from "$lib/utils/auth";
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

  return {
    title: `${service.name} | ${service.structureInfo.name} | DORA`,
    description: service.shortDesc,
    service,
    structure: await getStructure(service.structure),
    servicesOptions: await getServicesOptions(),
  };
};
