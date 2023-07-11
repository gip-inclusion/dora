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
  extraRecipients: string[],
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
      extraRecipients,
      message,
    }),
  });
}

export function contactService(
  queryId: string,
  extraRecipients: string[],
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
      extraRecipients,
      message,
    }),
  });
}

export function denyOrientation(
  queryId: string,
  reason: string,
  otherDetails?: string
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
      reason,
      otherDetails,
    }),
  });
}

export function acceptOrientation(
  queryId: string,
  {
    response,
    orientationStartDate,
    orientationEndDate,
    orientationLocation,
    addBeneficiaryMessage,
    beneficiaryMessage,
  }: {
    response: string;
    orientationStartDate: string;
    orientationEndDate: string;
    orientationLocation: string;
    addBeneficiaryMessage: string[];
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
      response,
      orientationStartDate,
      orientationEndDate,
      orientationLocation,
      addBeneficiaryMessage,
      beneficiaryMessage,
    }),
  });
}
