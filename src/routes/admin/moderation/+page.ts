import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Modération | Administration | DORA",
    noIndex: true,
  };
};
