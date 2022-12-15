import { browser } from "$app/environment";
import { getMembers, getPutativeMembers } from "$lib/requests/structures";
import { userInfo } from "$lib/utils/auth";
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

  const info = get(userInfo);
  const struct = get(structure);

  const canSeeMembers = struct.isMember || info?.isBizdev || info?.isStaff;
  const canEditMembers = struct.isAdmin || info?.isBizdev || info?.isStaff;

  if (!info || !struct || !canSeeMembers) {
    throw error(404, "Page Not Found");
  }

  const members = await getMembers(struct.slug);
  const putativeMembers = await getPutativeMembers(struct.slug);

  return {
    title: `Collaborateurs | ${capitalize(struct.name)} | DORA`,
    description: struct.shortDesc,
    members,
    putativeMembers,
    canSeeMembers,
    canEditMembers,
  };
};
