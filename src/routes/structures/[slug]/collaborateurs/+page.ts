import { browser } from "$app/environment";
import { userInfo } from "$lib/utils/auth";
import { capitalize } from "$lib/utils/misc";
import { error } from "@sveltejs/kit";
import { get } from "svelte/store";
import { structure } from "../store";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ parent }) => {
  const { members, putativeMembers } = await parent();

  // sur le serveur, info est toujours null,
  // on retourne une 404 uniquement sur le client
  if (!browser) {
    return {};
  }

  const info = get(userInfo);
  const struct = get(structure);

  if (!info || !struct || !struct.canViewMembers) {
    throw error(404, "Page Not Found");
  }

  return {
    title: `Collaborateurs | ${capitalize(struct.name)} | DORA`,
    description: struct.shortDesc,
    members,
    putativeMembers,
  };
};
