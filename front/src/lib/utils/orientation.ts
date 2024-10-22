import { getApiURL } from "./api";
import { fetchData } from "./misc";
import type { Choice, Orientation, Service } from "$lib/types";

export function getOrientation(queryId: string, queryHash: string) {
  return fetchData<Orientation>(
    `${getApiURL()}/orientations/${queryId}/?h=${queryHash}`
  );
}

export async function refreshOrientationLink(queryId: string) {
  const url = `${getApiURL()}/orientations/${queryId}/refresh/`;
  const method = "PATCH";
  await fetch(url, {
    method,
  });
}

export function contactBeneficiary(
  queryId: string,
  queryHash: string,
  ccPrescriber: boolean,
  ccReferent: boolean,
  message: string
) {
  const url = `${getApiURL()}/orientations/${queryId}/contact/beneficiary/?h=${queryHash}`;
  const method = "POST";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ccPrescriber,
      ccReferent,
      message,
    }),
  });
}

export function contactPrescriber(
  queryId: string,
  queryHash: string,
  ccBeneficiary: boolean,
  ccReferent: boolean,
  message: string
) {
  const url = `${getApiURL()}/orientations/${queryId}/contact/prescriber/?h=${queryHash}`;
  const method = "POST";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ccBeneficiary,
      ccReferent,
      message,
    }),
  });
}

export function denyOrientation(
  queryId: string,
  queryHash: string,
  { reasons, message }: { reasons: string[]; message: string }
) {
  const url = `${getApiURL()}/orientations/${queryId}/reject/?h=${queryHash}`;
  const method = "POST";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      reasons,
      message,
    }),
  });
}

export function acceptOrientation(
  queryId: string,
  queryHash: string,
  {
    message,
    beneficiaryMessage,
  }: {
    message: string;
    beneficiaryMessage: string;
  }
) {
  const url = `${getApiURL()}/orientations/${queryId}/validate/?h=${queryHash}`;
  const method = "POST";
  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      beneficiaryMessage,
    }),
  });
}

export function computeConcernedPublicChoices(service: Service): {
  concernedPublicChoices: Choice[];
  concernedPublicRequired: boolean;
} {
  const excludedConcernedPublicLabels = ["Autre", "Tous publics"];
  const concernedPublicChoices = (service.concernedPublicDisplay || [])
    .map((value) => ({ value: value, label: value }))
    .filter((elt) => !excludedConcernedPublicLabels.includes(elt.value));

  return {
    concernedPublicChoices,
    concernedPublicRequired:
      concernedPublicChoices.filter((elt) => elt.value !== "Autre").length > 0,
  };
}

export function computeRequirementsChoices(service: Service): {
  requirementChoices: Choice[];
  requirementRequired: boolean;
} {
  const excludedRequirementLabels = ["Aucun", "Sans condition"];

  const requirementChoices = [
    ...(service.requirementsDisplay || []),
    ...(service.accessConditionsDisplay || []),
  ]
    .map((value) => ({ value: value, label: value }))
    .filter((elt) => !excludedRequirementLabels.includes(elt.value));

  return {
    requirementChoices,
    requirementRequired: requirementChoices.length > 0,
  };
}
