import type { Establishment } from "$lib/types";
import { getApiURL } from "$lib/utils/api";
import type { PageLoad } from "./$types";

function siretSearch(siret: string) {
  const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(siret)}`;

  return fetch(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

export const load: PageLoad = async ({ url }) => {
  const siret = url.searchParams.get("siret");
  let establishment: Establishment | undefined;
  if (siret) {
    const response = await siretSearch(siret);
    if (response.status === 200) {
      establishment = (await response.json()) as Establishment;
    }
  }
  return {
    title: "Rattachement à votre structure | DORA",
    noIndex: true,
    establishment,
  };
};
