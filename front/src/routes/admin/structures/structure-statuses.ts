import type { AdminStructure } from "$lib/types";

import { getStructureStatus } from "./structures-filters";

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

// On utilise les mêmes règles que pour les filtres de statut du tableau de bord.
function getAdminsBadge(structure: AdminStructure): StructureStatusBadge {
  const status = getStructureStatus(structure);

  if (status === "awaitingModeration") {
    return { label: "Administrateur à valider", color: "orange" };
  }
  if (status === "waiting") {
    return { label: "Administrateur invité", color: "orange" };
  }
  if (!structure.hasAdmin) {
    return { label: "Sans administrateur", color: "red" };
  }
  return { label: "Administrateur validé", color: "green" };
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
