import { getServiceAdmin } from "$lib/requests/admin";
import { error } from "@sveltejs/kit";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const service = await getServiceAdmin(params.slug);
  if (!service) {
    throw error(404, "Page Not Found");
  }

  return {
    title: `${service.name} | Administration | DORA`,
    noIndex: true,
    service: service,
  };
};
