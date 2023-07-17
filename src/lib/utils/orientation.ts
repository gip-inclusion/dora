import { getApiURL } from "./api";
import { fetchData } from "./misc";
import type { Orientation } from "$lib/types";

export async function getOrientation(
  queryId: string
): Promise<Orientation | null> {
  const url = `${getApiURL()}/orientations/${queryId}/`;

  return (await fetchData<Orientation>(url)).data;
}

export function contactBeneficiary(
  queryId: string,
  ccPrescriber: boolean,
  ccReferent: boolean,
  message: string
) {
  const url = `${getApiURL()}/orientations/${queryId}/contact/beneficiary/`;
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
  ccBeneficiary: boolean,
  ccReferent: boolean,
  message: string
) {
  const url = `${getApiURL()}/orientations/${queryId}/contact/prescriber/`;
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
  { reasons, message }: { reasons: string[]; message: string }
) {
  const url = `${getApiURL()}/orientations/${queryId}/reject/`;
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
  {
    message,
    beneficiaryMessage,
  }: {
    message: string;
    beneficiaryMessage: string;
  }
) {
  const url = `${getApiURL()}/orientations/${queryId}/validate/`;
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
