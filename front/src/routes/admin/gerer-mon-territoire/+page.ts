import { getDepartments } from "$lib/requests/geo";
import { userInfo } from "$lib/utils/auth";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch, parent }) => {
  await parent();

  const user = get(userInfo);

  // Sans département renseigné (cas du staff), tous les départements sont retournés.
  const departments = await getDepartments(user?.departments ?? [], fetch);

  if (!departments.length) {
    error(403, "Accès réservé");
  }

  return {
    title: "Gérer mon territoire | DORA",
    noIndex: true,
    departments,
    // Le premier des départements couverts par le gestionnaire est affiché directement.
    department: departments[0].value,
  };
};
