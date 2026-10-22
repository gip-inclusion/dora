import { getPartners } from "#lib/utils/partners.ts";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = () => {
  return {
    title: "Nos partenaires | DORA",
    partnersToShow: getPartners(),
  };
};
