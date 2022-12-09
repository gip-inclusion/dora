import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Mon compte | DORA",
    noIndex: true,
  };
};
