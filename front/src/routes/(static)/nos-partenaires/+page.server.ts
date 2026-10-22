import { getPartners } from "#lib/utils/partners.js";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = () => {
  return {
    title: "Nos partenaires | DORA",
    partnersToShow: getPartners(),
  };
};
