import type { AdminStructure } from "$lib/types";

import { getStatusLabel, getStructureStatus } from "./structures-filters";

export type StructureStatusColor = "green" | "orange" | "red" | "gray";

export const STATUS_DOT_COLORS: Record<StructureStatusColor, string> = {
  green: "bg-success",
  orange: "bg-warning",
  red: "bg-error",
  gray: "bg-gray-text-alt",
};

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
export function getAdminsBadge(
  structure: AdminStructure
): StructureStatusBadge {
  const status = getStructureStatus(structure);

  if (status === "awaitingModeration" || status === "waiting") {
    return { label: getStatusLabel(status), color: "orange" };
  }
  if (!structure.hasAdmin) {
    return { label: getStatusLabel("orphan"), color: "red" };
  }
  return { label: "Administrateur validé", color: "green" };
}

// Indique que le statut mis en avant concerne les administrateurs de la structure.
export function hasAdminStatus(structure: AdminStructure): boolean {
  return !structure.isObsolete && getAdminsBadge(structure).color !== "green";
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
