import type { PageLoad } from "./$types";
import { getServicesAdmin } from "$lib/requests/admin";

export const load: PageLoad = ({ fetch }) => {
  return {
    services: getServicesAdmin(fetch),
    title: "Services | Administration | DORA",
    noIndex: true,
  };
};
