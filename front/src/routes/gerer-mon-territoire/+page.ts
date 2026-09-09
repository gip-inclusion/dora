import { getDepartments } from "$lib/requests/geo";
import { isAuthenticated, userInfo } from "$lib/utils/auth";
import { error, redirect } from "@sveltejs/kit";
import { get } from "svelte/store";
import type { PageLoad } from "./$types";

// Car il s'agit d'une page authentifiée.
export const ssr = false;

export const load: PageLoad = async ({ fetch, parent, url }) => {
  await parent();

  if (!isAuthenticated()) {
    redirect(
      302,
      `/auth/connexion?next=${encodeURIComponent(url.pathname + url.search)}`
    );
  }

  const user = get(userInfo);

  if (!user?.isManager || !user.departments?.length) {
    error(403, "Accès réservé");
  }

  const departments = await getDepartments(user.departments, fetch);

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
