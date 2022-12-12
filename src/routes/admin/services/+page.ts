import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Services | Administration | DORA",
    noIndex: true,
  };
};
