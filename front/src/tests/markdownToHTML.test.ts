import { htmlToMarkdown } from "#lib/utils/html-to-markdown.ts";
import { markdownToHTML } from "#lib/utils/markdown.ts";
import sanitizeHtml from "sanitize-html";
import { describe, expect, test } from "vitest";

const textOnly = (html: string) =>
  sanitizeHtml(html, { allowedTags: [], allowedAttributes: {} }).replace(
    /\s/gu,
    ""
  );

describe("markdownToHTML", () => {
  test.each([null, undefined, ""])("contenu vide : %s", (value) => {
    expect(markdownToHTML(value)).toBe("");
  });

  test("conservation du titre des liens", () => {
    expect(markdownToHTML('[a](https://x.fr "titre")')).toBe(
      '<p><a href="https://x.fr" title="titre" target="_blank" rel="noopener noreferrer">a</a></p>'
    );
  });

  test("conversion basique", () => {
    expect(markdownToHTML("**bb**")).toBe("<p><strong>bb</strong></p>");
  });

  test("paragraphes, emphase et retour à la ligne simple", () => {
    expect(
      markdownToHTML(
        "Texte **gras** et *italique*.\n\nSecond paragraphe\navec retour simple."
      )
    ).toBe(
      "<p>Texte <strong>gras</strong> et <em>italique</em>.</p>\n<p>Second paragraphe\navec retour simple.</p>"
    );
  });

  test("listes", () => {
    expect(markdownToHTML("- un\n- deux\n\n1. a\n2. b")).toBe(
      "<ul>\n<li>un</li>\n<li>deux</li>\n</ul>\n<ol>\n<li>a</li>\n<li>b</li>\n</ol>"
    );
  });

  test("tableaux", () => {
    expect(markdownToHTML("| a | b |\n|---|---|\n| 1 | 2 |")).toBe(
      "<table>\n<thead>\n<tr>\n<th>a</th>\n<th>b</th>\n</tr>\n</thead>\n<tbody><tr>\n<td>1</td>\n<td>2</td>\n</tr>\n</tbody></table>"
    );
  });

  test("ajout des `rel='noopener noreferrer'`", () => {
    const text = `[https://perdu.com/](Perdu) - [https://www.google.fr/](Google)`;

    expect(markdownToHTML(text)).toBe(
      '<p><a href="Perdu" target="_blank" rel="noopener noreferrer">https://perdu.com/</a> - <a href="Google" target="_blank" rel="noopener noreferrer">https://www.google.fr/</a></p>'
    );
  });

  test("liens automatiques, sans la ponctuation finale", () => {
    expect(
      markdownToHTML(
        "Voir https://exemple.fr, www.exemple.fr ou contact@exemple.fr."
      )
    ).toBe(
      '<p>Voir <a href="https://exemple.fr" target="_blank" rel="noopener noreferrer">https://exemple.fr</a>, <a href="http://www.exemple.fr" target="_blank" rel="noopener noreferrer">www.exemple.fr</a> ou <a href="mailto:contact@exemple.fr" target="_blank" rel="noopener noreferrer">contact@exemple.fr</a>.</p>'
    );
  });

  test("pas d'ajout des `rel='nofollow'` si le href n'est pas précédé d'un espace", () => {
    const text = `to_href="#"`;
    expect(markdownToHTML(text)).toBe(`<p>${text}</p>`);
    expect(markdownToHTML(text)).not.contains("noopener");
    expect(markdownToHTML(text)).not.contains("noreferrer");
  });

  test("identifiant de titre", () => {
    expect(markdownToHTML("## Article 9 {accord_co_responsabilite}")).toBe(
      '<h2 id="accord_co_responsabilite">Article 9</h2>'
    );
  });

  test("identifiant de titre sans coût quadratique", () => {
    const start = performance.now();
    markdownToHTML(`# a${" ".repeat(50_000)}b`);
    expect(performance.now() - start).toBeLessThan(100);
  });

  test("bon niveau de titre", () => {
    const text = `# titre1\n## titre2`;
    expect(markdownToHTML(text)).toBe("<h1>titre1</h1>\n<h2>titre2</h2>");
    expect(markdownToHTML(text, 1)).toBe("<h1>titre1</h1>\n<h2>titre2</h2>");
    expect(markdownToHTML(text, 2)).toBe("<h2>titre1</h2>\n<h3>titre2</h3>");
    expect(markdownToHTML(text, 3)).toBe("<h3>titre1</h3>\n<h4>titre2</h4>");
    expect(markdownToHTML(text, 4)).toBe("<h4>titre1</h4>\n<h5>titre2</h5>");
    expect(markdownToHTML(text, 5)).toBe("<h5>titre1</h5>\n<h6>titre2</h6>");
    expect(markdownToHTML("###### titre6", 3)).toBe("<h6>titre6</h6>");
  });

  test.each([
    ["** Points étudiés** :", "<p> <strong>Points étudiés</strong> :</p>"],
    ["un **mot ** ici", "<p>un <strong>mot</strong>  ici</p>"],
    [
      "**gras** suite **autre**",
      "<p><strong>gras</strong> suite <strong>autre</strong></p>",
    ],
    [
      "** a**\n\n**b **",
      "<p> <strong>a</strong></p>\n<p><strong>b</strong> </p>",
    ],
    ["texte ** isolé", "<p>texte ** isolé</p>"],
    ["2 ** 3 ** 4", "<p>2 ** 3 ** 4</p>"],
  ])("gras avec espace collé au délimiteur : %s", (markdown, html) => {
    expect(markdownToHTML(markdown)).toBe(html);
  });

  test.each([
    ["<script>alert(1)</script>", ""],
    ["<img src=x onerror=alert(1)>", '<img src="x" />'],
    [
      '<a href="javascript:alert(1)">x</a>',
      '<p><a target="_blank" rel="noopener noreferrer">x</a></p>',
    ],
    ['<iframe src="https://exemple.fr"></iframe>', ""],
    ['<p style="color:red" onclick="alert(1)">p</p>', "<p>p</p>"],
    [
      '<svg><a href="javascript:alert(1)">x</a></svg>',
      '<p><a target="_blank" rel="noopener noreferrer">x</a></p>',
    ],
    [
      '<a href="https://exemple.fr" class="btn">x</a>',
      '<p><a href="https://exemple.fr" target="_blank" rel="noopener noreferrer">x</a></p>',
    ],
  ])("nettoyage de %s", (html, expected) => {
    expect(markdownToHTML(html)).toBe(expected);
  });
});

describe("htmlToMarkdown", () => {
  test.each([
    "# Titre\n\nTexte **gras** et *italique*.",
    "- un\n- deux",
    "[site](https://dora.fr)",
  ])("aller-retour sans perte : %s", (markdown) => {
    const html = markdownToHTML(markdown);
    expect(markdownToHTML(htmlToMarkdown(html))).toBe(html);
  });

  test.each([
    ["<p>Intro :</p><ul><li><p>un</p></li><li><p>deux</p></li></ul>", "<li>"],
    ["<ol><li><p>a</p></li><li><p>b</p></li></ol>", "<ol>"],
    ["<ul><li><p>un</p><ul><li><p>sous</p></li></ul></li></ul>", "<ul>"],
  ])("conversion du HTML de Tiptap sans perte : %s", (html, tag) => {
    const rendered = markdownToHTML(htmlToMarkdown(html));
    expect(rendered).toContain(tag);
    expect(textOnly(rendered)).toBe(textOnly(html));
  });

  test.each([
    ["<p>2024. Bilan</p>", "2024\\. Bilan"],
    ["<p># tag</p>", "\\# tag"],
    ["<p>- note</p>", "\\- note"],
    ["<p>snake_case</p>", "snake\\_case"],
  ])("le texte saisi n'est pas réinterprété : %s", (html, markdown) => {
    expect(htmlToMarkdown(html)).toBe(markdown);
    expect(markdownToHTML(markdown)).toBe(html);
  });

  test("barré et souligné conservés", () => {
    const html = "<p>a <s>barré</s> <u>souligné</u></p>";
    expect(markdownToHTML(htmlToMarkdown(html))).toBe(html);
  });

  test("le gras de Tiptap ne garde pas d'espace collé au délimiteur", () => {
    expect(
      htmlToMarkdown(
        '<p>a <strong> b</strong> <a class="underline" href="https://x.fr">x</a></p>'
      )
    ).toBe("a **b** [x](https://x.fr)");
  });
});
