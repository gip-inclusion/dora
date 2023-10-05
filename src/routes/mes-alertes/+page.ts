import type { PageLoad } from "./$types";

export const ssr = false;

export const load: PageLoad = () => {
  return {
    title: "Mes alertes | DORA",
    noIndex: true,
  };
};
