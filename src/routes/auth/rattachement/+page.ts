import type { PageLoad } from "./$types";

export const load: PageLoad = async () => {
  return {
    title: "Rattachement à votre structure | DORA",
    noIndex: true,
  };
};
