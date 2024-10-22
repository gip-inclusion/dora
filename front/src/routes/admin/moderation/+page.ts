import type { PageLoad } from "./$types";

export const load: PageLoad = () => {
  return {
    title: "Modération | Administration | DORA",
    noIndex: true,
  };
};
