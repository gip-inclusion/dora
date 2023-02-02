import type { PageLoad } from "../../../../.svelte-kit/types/src/routes";

export const load: PageLoad = () => {
  return {
    title: "Déclaration d’accessibilité",
    noIndex: true,
  };
};
