import type { SearchQuery } from "$lib/types";
import { logException } from "./logger";

const LAST_SEARCH_CITY_KEY = "lastSearch";

export function getQuery({
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  feeConditions,
  kindIds,
}: SearchQuery) {
  const parameters = {
    cats: categoryIds.join(","),
    subs: subCategoryIds.join(","),
    city: cityCode,
    cl: cityLabel,
    kinds: kindIds.join(","),
    fees: feeConditions.join(","),
  };
  const query = Object.entries(parameters)
    .filter(([_k, v]) => !!v)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");

  return query;
}

export function storeLastSearchCity(cityCode, cityLabel) {
  localStorage.setItem(
    LAST_SEARCH_CITY_KEY,
    JSON.stringify({
      cityCode,
      cityLabel,
    })
  );
}

export function getLastSearchCity() {
  let cityCode, cityLabel;
  const lastSearch = localStorage.getItem(LAST_SEARCH_CITY_KEY);
  if (lastSearch) {
    try {
      ({ cityCode, cityLabel } = JSON.parse(lastSearch));
    } catch (err) {
      logException(err, "Impossible de lire la dernière ville de recherche");
    }
  }
  return { cityCode, cityLabel };
}
