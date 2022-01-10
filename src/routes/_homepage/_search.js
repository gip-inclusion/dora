export function getQuery(category, subcategory, cityCode, radius, cityLabel) {
  const parameters = {
    cat: category,
    sub: subcategory,
    city: cityCode,
    cl: cityLabel,
    radius,
  };
  const query = Object.entries(parameters)
    .filter(([_k, v]) => v != null)
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join("&");

  return query;
}
