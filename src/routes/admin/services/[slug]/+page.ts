import { error } from "@sveltejs/kit";
import { getServiceAdmin } from "$lib/admin";

export async function load({ params, parent }) {
  await parent();

  const service = await getServiceAdmin(params.slug);
  if (!service) {
    throw error(404, "Page Not Found");
  }

  return {
    service: service,
  };
}
