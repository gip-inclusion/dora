import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Déclaration d’accessibilité",
    noIndex: true,
  };
};
