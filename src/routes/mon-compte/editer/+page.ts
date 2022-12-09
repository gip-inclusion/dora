import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Éditer | Mon compte | DORA",
    noIndex: true,
  };
};
