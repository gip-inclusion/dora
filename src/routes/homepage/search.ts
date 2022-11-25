import type { SearchQuery } from "$lib/types";

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
