import { browser } from "$app/environment";
import {
  getService,
  getServiceDI,
  getServicesOptions,
} from "$lib/requests/services";
import type { Service } from "$lib/types";
import { token } from "$lib/utils/auth";
import { error, redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, url, params, parent }) => {
  await parent();

  if (params.slug.startsWith("di--")) {
    const service = (await getServiceDI(params.slug.slice(4))) as Service;
    if (!service) {
      error(404, "Page Not Found");
    }

    return {
      title: `${service.name} | ${service.structureInfo.name} | DORA`,
      description: service.shortDesc,
      service,
      servicesOptions: await getServicesOptions(fetch),
      isDI: true,
      noIndex: true,
    };
  }

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
      redirect(
        302,
        `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
      );
    }
    error(404, "Page Not Found");
  }

  return {
    title: `${service.name} | ${service.structureInfo.name} | DORA`,
    description: service.shortDesc,
    service,
    servicesOptions: await getServicesOptions(fetch),
  };
};
