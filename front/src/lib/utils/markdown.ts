import { Marked } from "marked";
import sanitizeHtml from "sanitize-html";

const MARKDOWN_SANITIZE_OPTIONS: sanitizeHtml.IOptions = {
  allowedTags: [...sanitizeHtml.defaults.allowedTags, "img", "del"],
  allowedAttributes: {
    ...sanitizeHtml.defaults.allowedAttributes,
    a: [...sanitizeHtml.defaults.allowedAttributes.a, "rel", "title"],
    ["h2"]: ["id"],
  },
  transformTags: {
    a: sanitizeHtml.simpleTransform("a", {
      target: "_blank",
      rel: "noopener noreferrer",
    }),
  },
};

// Identifiant de titre à la fin du titre (`## Article 9 {accord_co_responsabilite}`),
// cible des liens `/cgu#accord_co_responsabilite`
const HEADING_ID_PATTERN = /\{([\w-]+)\}$/u;

const marked = new Marked({
  renderer: {
    heading({ tokens, depth }) {
      const html = this.parser.parseInline(tokens);
      const id = HEADING_ID_PATTERN.exec(html)?.[1];
      const content = id
        ? html.replace(HEADING_ID_PATTERN, "").trimEnd()
        : html;
      return `<h${depth}${id ? ` id="${id}"` : ""}>${content}</h${depth}>\n`;
    },
  },
});

// L'ancien éditeur (showdown) écrivait `** gras**` quand l'espace précédant le
// mot était mis en gras : CommonMark n'y voit pas de gras et afficherait les
// astérisques. On sort donc l'espace des délimiteurs appariés, sauf s'il y en a
// des deux côtés (`2 ** 3 ** 4`), que showdown ne mettait pas non plus en gras.
function normalizeSpacedBold(markdown: string) {
  return markdown
    .replace(/\r\n?/gu, "\n")
    .split("\n\n")
    .map((paragraph) => {
      const parts = paragraph.split("**");
      for (let i = 1; i < parts.length - 1; i += 2) {
        const trimmed = parts[i].trim();
        const start = parts[i].indexOf(trimmed);
        const end = start + trimmed.length;
        if (trimmed && (start === 0) !== (end === parts[i].length)) {
          parts[i - 1] += parts[i].slice(0, start);
          parts[i + 1] = parts[i].slice(end) + parts[i + 1];
          parts[i] = trimmed;
        }
      }
      return parts.join("**");
    })
    .join("\n\n");
}

export function markdownToHTML(
  markdownContent: string | null | undefined,
  titleLevel = 1
) {
  const tokens = marked.lexer(normalizeSpacedBold(markdownContent ?? ""));
  // Décale les titres pour les insérer dans la hiérarchie de la page
  marked.walkTokens(tokens, (token) => {
    if (token.type === "heading") {
      token.depth = Math.min(token.depth + titleLevel - 1, 6);
    }
  });
  return sanitizeHtml(marked.parser(tokens), MARKDOWN_SANITIZE_OPTIONS).trim();
}
