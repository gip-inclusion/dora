import { redirect } from "@sveltejs/kit";

import type { PageLoad } from "./$types";

// Ancienne recherche par mots-clés (Google CSE), conservée pour les favoris.
export const load: PageLoad = () => {
  redirect(301, "/recherche-mots-cles");
};
