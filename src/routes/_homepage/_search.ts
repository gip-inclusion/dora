export function getQuery({
  categoryIds,
  subCategoryIds,
  cityCode,
  cityLabel,
  kindId,
  fee,
}: {
  categoryIds: string[];
  subCategoryIds: string[];
  cityCode: string;
  cityLabel: string;
  kindId?: string;
  fee?: string[];
}) {
  const parameters = {
    cat: categoryIds,
    sub: subCategoryIds,
    city: cityCode,
    cl: cityLabel,
    kinds: kindId,
    fee: undefined,
  };

  if (fee?.length) {
    parameters.fee = fee;
  }

  const query = Object.entries(parameters)
    .filter(([_k, v]) => !!v)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");

  return query;
}
