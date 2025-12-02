import type { SavedSearch, SavedSearchNotificationFrequency } from "$lib/types";
import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import { getToken } from "$lib/utils/auth";
import { getQueryString } from "$lib/utils/service-search";

export async function saveSearch(
  savedSearch: Pick<
    SavedSearch,
    | "cityCode"
    | "cityLabel"
    | "category"
    | "subcategories"
    | "kinds"
    | "fees"
    | "locationKinds"
    | "fundingLabels"
  >
) {
  const url = `${getApiURL()}/saved-searches/`;
  const method = "POST";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${getToken()}`,
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
      Authorization: `Token ${getToken()}`,
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
      Authorization: `Token ${getToken()}`,
    },
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function getRecentSearchResults(
  savedSearchId: number,
  fetchFunction = fetch
) {
  const url = `${getApiURL()}/saved-searches/${savedSearchId}/recent/`;

  const response = await fetchData<SavedSearch[]>(url, fetchFunction);
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
    kindIds: savedSearch.kinds.sort(),
    feeConditions: savedSearch.fees.sort(),
    locationKinds: savedSearch.locationKinds.sort(),
    fundingLabels: savedSearch.fundingLabels.sort(),
  });
}
