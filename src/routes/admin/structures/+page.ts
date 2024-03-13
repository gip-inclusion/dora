import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getApiURL } from "$lib/utils/api";
import type { GeoApiValue } from "$lib/types";
import { error } from "@sveltejs/kit";

async function getDepartments(departmentCodes) {
  const url = `${getApiURL()}/admin-division-departments/?dept_codes=${encodeURIComponent(
    departmentCodes.join(",")
  )}`;
  const response = await fetch(url);
  const jsonResponse = await response.json();
  const results = jsonResponse.map((result) => ({
    value: result,
    label: `${result.name} (${result.code})`,
  }));
  return results;
}

export const load: PageLoad = async ({ parent }) => {
  await parent();

  const [servicesOptions, structuresOptions] = await Promise.all([
    getServicesOptions(),
    getStructuresOptions(),
  ]);

  const user = get(userInfo);

  let department;
  let departments: GeoApiValue[] = [];
  let title = "Structures | Administration | DORA";
  if (user.isManager) {
    departments = await getDepartments(user.departments);
    [department] = departments;
    if (!department) {
      error(403, "Accès réservé");
    }
    department = department.value;
    title = `Tableau de bord ${user.departments} | DORA`;
  }

  return {
    title,
    noIndex: true,
    servicesOptions,
    structuresOptions,
    isManager: user.isManager && department,
    department,
    departments,
  };
};
