import { getServicesOptions } from "$lib/requests/services";
import { getStructuresOptions } from "$lib/requests/structures";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { getApiURL } from "$lib/utils/api";

async function searchAdminDivision(query) {
  const url = `${getApiURL()}/admin-division-search/?type=department&q=${encodeURIComponent(
    query
  )}&with_geom=1`;
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
  let title = "Structures | Administration | DORA";
  if (user.isManager) {
    department = (await searchAdminDivision(user.department))[0].value;
    title = `Tableau de bord ${user.department} | DORA`;
  }
  return {
    title,
    noIndex: true,
    servicesOptions,
    structuresOptions,
    isManager: user.isManager && department,
    department,
  };
};
