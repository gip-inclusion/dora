import type { PageLoad } from "./$types";
import content from "./content.md?raw";

export const load: PageLoad = () => {
  return {
    title: "Conditions générales d’utilisation | DORA",
    noIndex: true,
    content,
  };
};
