import { error } from "@sveltejs/kit";
import type { Service } from "#lib/types.ts";
import { getService, getServiceDI } from "#lib/requests/services.ts";
import type { LayoutLoad } from "./$types";

export const ssr = false;

export const load: LayoutLoad = async ({ fetch, params, parent }) => {
  await parent();

  const service = params.slug.startsWith("di--")
    ? ((await getServiceDI(params.slug.slice(4), fetch)) as Service)
    : await getService(params.slug, fetch);

  if (!service) {
    error(404, "Page Not Found");
  }

  return { service };
};
