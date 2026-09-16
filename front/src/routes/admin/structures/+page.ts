import { getDepartments } from "$lib/requests/geo";
import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getInitialDepartment } from "$lib/utils/manager-department";
import { error } from "@sveltejs/kit";
import { parseStatusFilter } from "./structures-filters";

export const load: PageLoad = async ({ fetch, parent, url }) => {
  await parent();

  const [servicesOptions, structuresOptions] = await Promise.all([
    getServicesOptions(fetch),
    getStructuresOptions(fetch),
  ]);

  const user = get(userInfo);

  // Sans département renseigné (cas du staff), tous les départements sont retournés.
  const departments = await getDepartments(user?.departments ?? [], fetch);

  if (!departments.length) {
    error(403, "Accès réservé");
  }

  const title = user?.isManager
    ? `Tableau de bord ${user.departments} | DORA`
    : "Structures | Administration | DORA";

  return {
    title,
    noIndex: true,
    // Permet de pointer directement sur un onglet depuis « Gérer mon territoire »
    initialStatus: parseStatusFilter(url.searchParams.get("statut")),
    servicesOptions,
    structuresOptions,
    department: getInitialDepartment(departments),
    departments,
  };
};
