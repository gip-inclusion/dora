import { markdownToHTML } from "$lib/utils/index";
import { describe, expect, test } from "vitest";

describe("markdownToHTML", () => {
  test("conversion basique", () => {
    expect(markdownToHTML("**bb**")).toBe("<p><strong>bb</strong></p>");
  });

  test("ajout des `rel='nofollow'`", () => {
    const text = `[https://perdu.com/](Perdu) - [https://www.google.fr/](Google)`;

    expect(markdownToHTML(text)).toBe(
      '<p><a href="Perdu" rel="nofollow">https://perdu.com/</a> - <a href="Google" rel="nofollow">https://www.google.fr/</a></p>'
    );
  });

  test("pas d'ajout des `rel='nofollow'` si le href n'est pas précédé d'un espace", () => {
    const text = `to_href="#"`;
    expect(markdownToHTML(text)).toBe(`<p>${text}</p>`);
    expect(markdownToHTML(text)).not.contains("nofollow");
  });

  test("bon niveau de titre", () => {
    const text = `#titre1\n##titre2`;
    expect(markdownToHTML(text)).toBe("<h2>titre1</h2>\n<h3>titre2</h3>");
    expect(markdownToHTML(text, 3)).toBe("<h3>titre1</h3>\n<h4>titre2</h4>");
    expect(markdownToHTML(text, 4)).toBe("<h4>titre1</h4>\n<h5>titre2</h5>");
    expect(markdownToHTML(text, 5)).toBe("<h5>titre1</h5>\n<h6>titre2</h6>");
  });
});
