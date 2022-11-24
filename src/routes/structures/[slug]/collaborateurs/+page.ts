import { error } from "@sveltejs/kit";
import { browser } from "$app/environment";
import { get } from "svelte/store";
import { userInfo } from "$lib/auth";
import { structure } from "../_store";

import { getMembers, getPutativeMembers } from "$lib/structures";

export async function load({ parent }) {
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
    members,
    putativeMembers,
    canSeeMembers,
    canEditMembers,
  };
}
