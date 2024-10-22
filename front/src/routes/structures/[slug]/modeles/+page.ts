import { browser } from "$app/environment";
import { capitalize } from "$lib/utils/misc";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import { structure } from "../store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  await parent();

  // sur le serveur, info est toujours null,
  // on retourne une 404 uniquement sur le client
  if (!browser) {
    return {};
  }

  const struct = get(structure);

  if (!struct || !struct.canEditServices) {
    error(404, "Page Not Found");
  }

  return {
    title: `Modèles | ${capitalize(struct.name)} | DORA`,
    description: struct.shortDesc,
  };
};
