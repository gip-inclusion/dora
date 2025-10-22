import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getApiURL } from "$lib/utils/api";
import type { GeoApiValue } from "$lib/types";
import { error } from "@sveltejs/kit";

async function getDepartments(departmentCodes: string[], fetch = window.fetch) {
  const url = `${getApiURL()}/admin-division-departments/?dept_codes=${encodeURIComponent(
    departmentCodes.join(",")
  )}`;
  const response = await fetch(url);
  const jsonResponse = (await response.json()) as GeoApiValue[];
  const results = jsonResponse.map((result) => ({
    value: result,
    label: `${result.name} (${result.code})`,
  }));
  return results;
}

type GetDepartmentsResults = Awaited<ReturnType<typeof getDepartments>>;

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  const [servicesOptions, structuresOptions] = await Promise.all([
    getServicesOptions(fetch),
    getStructuresOptions(),
  ]);

  const user = get(userInfo);

  let departments: GetDepartmentsResults = [];
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
    servicesOptions,
    structuresOptions,
    isManager: Boolean(user.isManager && department),
    department,
    departments,
  };
};
