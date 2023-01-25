import type { PageLoad } from "./$types";
import content from "./content.md?raw";

export const load: PageLoad = () => {
  return {
    title: "Mentions légales | DORA",
    noIndex: true,
    content,
  };
};
