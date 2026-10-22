import { getPartners } from "#lib/utils/partners.ts";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = () => {
  return {
    partnersToShow: getPartners(6),
  };
};
