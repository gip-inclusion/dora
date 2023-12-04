import type { Establishment } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import type { PageLoad } from "./$types";
import { userInfo } from "$lib/utils/auth";
import { get } from "svelte/store";

function siretSearch(siret: string) {
  const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(siret)}`;

  return fetch(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

function safirSearch(safir: string) {
  const url = `${getApiURL()}/search-safir/?safir=${encodeURIComponent(safir)}`;

  return fetch(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

export const load: PageLoad = async ({ url, parent }) => {
  await parent();
  const userEmail = get(userInfo).email;
  const userIsPe =
    userEmail.endsWith("@pole-emploi.fr") ||
    userEmail.endsWith("@beta.gouv.fr");

  let establishment: Establishment | undefined;

  const proposedSiret = url.searchParams.get("siret");
  const proposedSafir = userIsPe ? url.searchParams.get("safir") : "";

  if (proposedSiret) {
    const response = await siretSearch(proposedSiret);
    if (response.status === 200) {
      establishment = (await response.json()) as Establishment;
    }
  } else if (proposedSafir) {
    const response = await safirSearch(proposedSafir);
    if (response.status === 200) {
      establishment = (await response.json()) as Establishment;
    }
  }
  return {
    title: "Rattachement à votre structure | DORA",
    noIndex: true,
    establishment,
    proposedSiret,
    proposedSafir,
    userIsPe,
  };
};
