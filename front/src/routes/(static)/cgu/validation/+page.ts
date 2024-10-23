import content from "../content.md?raw";
import type { PageLoad } from "./$types";
import { getNextPage } from "../../../auth/utils";

export const load: PageLoad = ({ url }) => {
  return {
    title: "Mise à jour des Conditions Générales d’Utilisation de DORA | DORA",
    noIndex: true,
    content,
    next: getNextPage(url),
  };
};
