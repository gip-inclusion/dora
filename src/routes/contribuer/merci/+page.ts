import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Merci de votre contribution | DORA",
    noIndex: true,
  };
};
