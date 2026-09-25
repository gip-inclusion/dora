import type { AdminStructure } from "$lib/types";
import type { StatusFilter } from "./types";

const STATUS_LABELS: Record<StatusFilter, string> = {
  all: "Toutes",
  orphan: "Sans administrateur",
  waiting: "Administrateur invité",
  awaitingModeration: "Administrateur à valider",
  awaitingActivation: "Sans service : non visible sur Dora",
  awaitingUpdate: "Service à actualiser",
  obsolete: "Désactivée",
};

// Onglets de filtrage du tableau de bord, dans l'ordre d'affichage. Le libellé
// vient de `STATUS_LABELS`, sauf lorsqu'un onglet a besoin du pluriel.
export const STATUS_FILTER_TABS: {
  status: StatusFilter;
  label: string;
  definition: string;
}[] = [
  {
    status: "all",
    label: STATUS_LABELS.all,
    definition: "Toutes les structures référencées par Dora sur le territoire",
  },
  {
    status: "orphan",
    label: STATUS_LABELS.orphan,
    definition: "Structures sans administrateur (ni actif ni invité)",
  },
  {
    status: "awaitingModeration",
    label: STATUS_LABELS.awaitingModeration,
    definition:
      "Structures avec un premier administrateur en attente de modération",
  },
  {
    status: "awaitingActivation",
    label: STATUS_LABELS.awaitingActivation,
    definition:
      "Structures avec (au moins) un administrateur validé mais sans service publié",
  },
  {
    status: "awaitingUpdate",
    label: STATUS_LABELS.awaitingUpdate,
    definition:
      "Structures avec (au moins) un service publié en attente d’actualisation",
  },
  {
    status: "obsolete",
    label: "Désactivées",
    definition:
      "Structures désactivées par l’équipe DORA ou un gestionnaire de territoire",
  },
];

export function getStructureStatus(
  struct: AdminStructure
): Exclude<StatusFilter, "all"> | undefined {
  // ⚠️ L'ordre des conditions est important
  if (struct.isObsolete) {
    return "obsolete";
  }
  if (struct.isWaiting) {
    return "waiting";
  }
  // Une structure peut n'avoir que des collaborateurs non administrateurs
  // (éventuellement non validés) alors que `hasAdmin` ne tient compte que des
  // administrateurs valides et actifs.
  if (!struct.hasAdmin) {
    return "orphan";
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

export function getStatusLabel(status?: StatusFilter): string {
  if (!status) {
    return "";
  }
  return STATUS_LABELS[status] ?? "";
}

export function getStatusDefinition(status: StatusFilter): string | undefined {
  return STATUS_FILTER_TABS.find((tab) => tab.status === status)?.definition;
}

export function parseStatusFilter(value: string | null): StatusFilter {
  return value && Object.hasOwn(STATUS_LABELS, value)
    ? (value as StatusFilter)
    : "all";
}
