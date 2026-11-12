// Conversion inverse, réservée à l'éditeur : dans un module séparé pour ne pas
// charger turndown sur les pages qui ne font qu'afficher du markdown
import { markdownToHTML } from "#lib/utils/markdown.ts";
import TurndownService from "turndown";

const turndownService = new TurndownService({
  headingStyle: "atx",
  bulletListMarker: "-",
  codeBlockStyle: "fenced",
  emDelimiter: "*",
});
// Garde en HTML le barré et le souligné de Tiptap, que turndown perdrait
turndownService.keep(["s", "u"]);

export function htmlToMarkdown(html: string) {
  return turndownService.turndown(html);
}

// Compare deux textes en markdown en ignorant les fins de ligne (`\r\n`), la forme des
// liens et les espaces en bord de texte, que l'éditeur réécrit à la première modification.
export function markdownCompare(a?: string | null, b?: string | null) {
  const rewrite = (value?: string | null) =>
    htmlToMarkdown(markdownToHTML(value ?? "")).trim();

  return rewrite(a) === rewrite(b);
}
