import { getApiURL } from "$lib/utils/api";
import type { PageLoad } from "./$types";

async function siretSearch(s) {
  const url = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(s)}`;

  return fetch(url, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}

export const load: PageLoad = async ({ url }) => {
  const siret = url.searchParams.get("siret");
  let establishment;
  if (siret) {
    const response = await siretSearch(siret);
    if (response.status === 200) {
      establishment = await response.json();
    }
  }
  return {
    title: "Rattachement à votre structure | DORA",
    noIndex: true,
    establishment,
  };
};
