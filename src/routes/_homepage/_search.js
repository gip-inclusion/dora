export function getQuery(category, subcategory, cityCode, cityLabel) {
  const parameters = {
    cat: category,
    sub: subcategory,
    city: cityCode,
    cl: cityLabel,
  };
  const query = Object.entries(parameters)
    .filter(([_k, v]) => v != null)
    .reduce((acc, [k, v]) => `${acc}${k}=${encodeURIComponent(v)}&`, "")
    .slice(0, -1);
  return query;
}
