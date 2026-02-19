import type { Establishment } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";

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
  const knownSiret = url.searchParams.get("known_siret") === "true";
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
    knownSiret,
    proposedSafir,
    userIsFranceTravail,
  };
};
