import { getServicesOptions } from "#lib/requests/services.ts";
import { getStructuresOptions } from "#lib/requests/structures.ts";
import type { PageLoad } from "./$types";
import { userInfo } from "#lib/utils/auth.ts";
import { get } from "svelte/store";
import { loadManagerDepartments } from "#lib/utils/manager-department.ts";

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  const [servicesOptions, structuresOptions, { departments, department }] =
    await Promise.all([
      getServicesOptions(fetch),
      getStructuresOptions(fetch),
      loadManagerDepartments(fetch),
    ]);

  const user = get(userInfo);

  const title = user?.isManager
    ? `Tableau de bord ${user.departments} | DORA`
    : "Structures | Administration | DORA";

  return {
    title,
    noIndex: true,
    servicesOptions,
    structuresOptions,
    department,
    departments,
  };
};
