import type {
  PutativeStructureMember,
  Structure,
  StructureMember,
} from "$lib/types";
import { structureSchema } from "$lib/validation/schemas/structure";
import { validate } from "$lib/validation/validation";

export function isStructureInformationsComplete(structure) {
  return validate(structure, structureSchema, {
    noScroll: true,
    showErrors: false,
  }).valid;
}
export function hasAtLeastOneServiceNotArchived(structure: Structure): boolean {
  // Note: `numServices` ne prend pas en compte les services archivés
  return structure.numServices > 0;
}
export function hasArchivedServices(structure: Structure): boolean {
  return structure.archivedServices.length > 0;
}

function hasAtLeastTwoMembers(members: Array<StructureMember> = []): boolean {
  return members.length > 1;
}
function hasInvitedMembers(
  putativeMembers: Array<PutativeStructureMember> = []
): boolean {
  return putativeMembers.filter((mbr) => mbr.invitedByAdmin).length > 0;
}

export function hasAtLeastTwoMembersOrInvitedMembers(members, putativeMembers) {
  return hasAtLeastTwoMembers(members) || hasInvitedMembers(putativeMembers);
}
