import type { AdminStructure } from "$lib/types";

export type StructureStatusColor = "green" | "orange" | "red" | "gray";

export interface StructureStatusBadge {
  label: string;
  color: StructureStatusColor;
}

function getServicesBadge(structure: AdminStructure): StructureStatusBadge {
  if (structure.numOutdatedServices > 0) {
    return { label: "Services à actualiser", color: "orange" };
  }
  if (structure.numPublishedServices === 0) {
    return { label: "Services à publier", color: "red" };
  }
  return { label: "Services publiés", color: "green" };
}

function getAdminsBadge(structure: AdminStructure): StructureStatusBadge {
  return structure.admins.length > 0
    ? { label: "Administrateur validé", color: "green" }
    : { label: "Administrateur à valider", color: "orange" };
}

export function getStructureStatusBadges(
  structure: AdminStructure
): StructureStatusBadge[] {
  // Une structure désactivée n'affiche aucun autre statut.
  if (structure.isObsolete) {
    return [{ label: "Structure désactivée", color: "gray" }];
  }

  return [getServicesBadge(structure), getAdminsBadge(structure)];
}
