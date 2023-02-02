import type { PageLoad } from "./$types";

export const load: PageLoad = () => {
  return {
    title: "Mes favoris | DORA",
    noIndex: true,
  };
};
