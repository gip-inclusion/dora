export const HOME_URL = "/";

export const HOME_SELECTORS = {};
HOME_SELECTORS.SEARCH_FORM = "#home-search-form";
HOME_SELECTORS.FORM_LABELS = `${HOME_SELECTORS.SEARCH_FORM} h4`;

/*
export async function fillSearchForm({
  page,
  category,
  subcategories,
  location,
}) {
  if (!Array.isArray(category)) category = [category];
  if (!Array.isArray(subcategories)) subcategories = [subcategories];

  // TODO: fill check form
}
*/
