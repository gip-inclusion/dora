import type { PageLoad } from "../../../../.svelte-kit/types/src/routes";
import content from "./content.md?raw";

export const load: PageLoad = () => {
  return {
    title: "Politique de confidentialité | DORA",
    noIndex: true,
    content,
  };
};
