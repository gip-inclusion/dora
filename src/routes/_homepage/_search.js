export function getQuery({
  categoryId,
  subCategoryId,
  cityCode,
  cityLabel,
  kindId,
  fee,
}) {
  const parameters = {
    cat: categoryId,
    sub: subCategoryId,
    city: cityCode,
    cl: cityLabel,
    kinds: kindId,
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
