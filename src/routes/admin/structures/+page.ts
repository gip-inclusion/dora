import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Structures | Administration | DORA",
    noIndex: true,
  };
};
