import type { PageLoad } from "./$types";
import content from "./content.md?raw";

export const load: PageLoad = () => {
  return {
    title: "Politique de confidentialité | DORA",
    noIndex: true,
    content,
  };
};
