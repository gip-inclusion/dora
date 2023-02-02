import type { PageLoad } from "./$types";

export const load: PageLoad = () => {
  return {
    title: "Mon compte | DORA",
    noIndex: true,
  };
};
