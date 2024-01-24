import { fetchData } from "$lib/utils/misc";
import { get } from "svelte/store";
import { token } from "../utils/auth";
import { getApiURL } from "../utils/api";
import type { SavedSearch, SavedSearchNotificationFrequency } from "$lib/types";
import { getQueryString } from "../utils/service-search";

export async function saveSearch(
  savedSearch: Pick<
    SavedSearch,
    "cityCode" | "cityLabel" | "category" | "subcategories" | "kinds" | "fees"
  >
) {
  const url = `${getApiURL()}/saved-searches/`;
  const method = "POST";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ ...savedSearch }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function updateSavedSearchFrequency(
  savedSearchId: number,
  frequency: SavedSearchNotificationFrequency
) {
  const url = `${getApiURL()}/saved-searches/${savedSearchId}/`;
  const method = "PATCH";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ frequency }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function deleteSavedSearch(savedSearchId: number) {
  const url = `${getApiURL()}/saved-searches/${savedSearchId}/`;
  const method = "DELETE";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function getRecentSearchResults(savedSearchId: number) {
  const url = `${getApiURL()}/saved-searches/${savedSearchId}/recent/`;

  const response = await fetchData<SavedSearch[]>(url);
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.data;
}

export function getSavedSearchQueryString(savedSearch: SavedSearch) {
  return getQueryString({
    categoryIds: [savedSearch.category],
    subCategoryIds: savedSearch.subcategories,
    cityCode: savedSearch.cityCode,
    cityLabel: savedSearch.cityLabel,
    label: savedSearch.label,
    kindIds: savedSearch.kinds,
    feeConditions: savedSearch.fees,
  });
}
