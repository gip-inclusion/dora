import { loadManagerDepartments } from "$lib/utils/manager-department";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  const { departments, department } = await loadManagerDepartments(fetch);

  return {
    title: "Gérer mon territoire | DORA",
    noIndex: true,
    departments,
    department,
  };
};
