export function getQuery(category, subcategory, cityCode, cityLabel) {
  const parameters = {
    cat: category,
    sub: subcategory,
    city: cityCode,
    cl: cityLabel,
  };
  const query = Object.entries(parameters)
    .filter(([_k, v]) => v != null)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");

  return query;
}
