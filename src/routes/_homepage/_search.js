export function getQuery({
  categoryId,
  subCategoryId,
  cityCode,
  cityLabel,
  kindId,
  hasNoFees,
}) {
  const parameters = {
    cat: categoryId,
    sub: subCategoryId,
    city: cityCode,
    cl: cityLabel,
    kinds: kindId,
  };

  if (hasNoFees) {
    // eslint-disable-next-line camelcase
    parameters.has_fee = "0";
  }

  const query = Object.entries(parameters)
    .filter(([_k, v]) => !!v)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");

  return query;
}
