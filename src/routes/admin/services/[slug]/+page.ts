import { getServiceAdmin } from "$lib/admin";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  await parent();

  const service = await getServiceAdmin(params.slug);
  if (!service) {
    throw error(404, "Page Not Found");
  }

  return {
    service: service,
  };
};
