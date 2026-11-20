import type { Orientation } from "#lib/types.ts";

import { getApiURL } from "./api";
import { fetchData } from "./misc";

export function getOrientation(
  queryId: string,
  queryHash: string,
  fetchFunction = fetch
) {
  return fetchData<Orientation>(
    `${getApiURL()}/orientations/${queryId}/?h=${queryHash}`,
    fetchFunction
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
