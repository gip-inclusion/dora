import { getDepartments, type DepartmentChoice } from "$lib/requests/geo";
import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import type { GeoApiValue } from "$lib/types";
import { error } from "@sveltejs/kit";
import { parseStatusFilter } from "./structures-filters";

export const load: PageLoad = async ({ fetch, parent, url }) => {
  await parent();

  const [servicesOptions, structuresOptions] = await Promise.all([
    getServicesOptions(fetch),
    getStructuresOptions(fetch),
  ]);

  const user = get(userInfo);

  let departments: DepartmentChoice[] = [];
  let department: GeoApiValue | undefined;
  let title = "Structures | Administration | DORA";

  if (user.isManager) {
    departments = await getDepartments(user.departments, fetch);
    if (departments.length === 0) {
      error(403, "Accès réservé");
    }
    department = departments[0].value;
    title = `Tableau de bord ${user.departments} | DORA`;
  }

  return {
    title,
    noIndex: true,
    // Permet de pointer directement sur un onglet depuis « Gérer mon territoire »
    initialStatus: parseStatusFilter(url.searchParams.get("statut")),
    servicesOptions,
    structuresOptions,
    isManager: Boolean(user.isManager && department),
    department,
    departments,
  };
};
