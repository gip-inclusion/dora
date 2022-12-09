import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Contribuer | DORA",
    description:
      "Aidez-nous à identifier et référencer l’ensemble de l’offre de l’insertion",
  };
};
