import type { AdminStructure } from "$lib/types";
import type { StatusFilter } from "./types";

const STATUS_LABELS: Record<StatusFilter, string> = {
  all: "Toutes",
  orphan: "Sans utilisateur",
  waiting: "Administrateur invité",
  expiredInvitation: "Invitation expirée",
  awaitingModeration: "À valider",
  awaitingActivation: "Sans service",
  awaitingUpdate: "Services à actualiser",
  obsolete: "Non conforme",
};

export function getStructureStatus(
  struct: AdminStructure
): Exclude<StatusFilter, "all"> | undefined {
  // ⚠️ L'ordre des conditions est important
  if (struct.isObsolete) {
    return "obsolete";
  }
  if (struct.isOrphan) {
    return struct.adminAlreadyInvited ? "expiredInvitation" : "orphan";
  }
  if (struct.isWaiting) {
    return "waiting";
  }
  if (struct.awaitingModeration) {
    return "awaitingModeration";
  }
  if (struct.awaitingActivation) {
    return "awaitingActivation";
  }
  if (struct.awaitingUpdate) {
    return "awaitingUpdate";
  }
  return undefined;
}

export function getStatusLabel(status: StatusFilter): string {
  return STATUS_LABELS[status];
}
