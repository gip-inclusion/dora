import type { PageLoad } from "../../../../.svelte-kit/types/src/routes";
import content from "./content.md?raw";

export const load: PageLoad = () => {
  return {
    title: "Mentions légales | DORA",
    noIndex: true,
    content,
  };
};
