import type { Establishment } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";

function siretSearch(siret: string, fetchFunction: typeof fetch) {
  const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(siret)}`;

  return fetchFunction(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

function safirSearch(safir: string, fetchFunction: typeof fetch) {
  const url = `${getApiURL()}/search-safir/?safir=${encodeURIComponent(safir)}`;

  return fetchFunction(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

export const load: PageLoad = async ({ fetch, url, parent }) => {
  await parent();
  const userEmail = get(userInfo)?.email;
  const userIsFranceTravail =
    userEmail?.endsWith("@pole-emploi.fr") ||
    userEmail?.endsWith("@francetravail.fr") ||
    userEmail?.endsWith("@beta.gouv.fr");

  let establishment: Establishment | undefined;

  const proposedSiret = url.searchParams.get("siret");
  const unknownSiret = url.searchParams.get("unknown_siret") === "true";
  const opJwt = url.searchParams.get(ORIENTATION_JWT_QUERY_PARAM);
  const serviceSlug = url.searchParams.get("service_slug");
  const isOrienter = url.searchParams.get("orienter") === "true";
  const proposedSafir = userIsFranceTravail
    ? url.searchParams.get("safir")
    : "";

  if (proposedSiret) {
    const response = await siretSearch(proposedSiret, fetch);
    if (response.status === 200) {
      establishment = (await response.json()) as Establishment;
    }
  } else if (proposedSafir) {
    const response = await safirSearch(proposedSafir, fetch);
    if (response.status === 200) {
      establishment = (await response.json()) as Establishment;
    }
  }
  return {
    title: "Rattachement à votre structure | DORA",
    noIndex: true,
    establishment,
    proposedSiret,
    unknownSiret,
    opJwt,
    serviceSlug,
    isOrienter,
    proposedSafir,
    userIsFranceTravail,
  };
};
