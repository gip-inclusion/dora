import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Contributions | Administration | DORA",
    noIndex: true,
  };
};
