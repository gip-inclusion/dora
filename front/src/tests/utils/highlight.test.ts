import { splitHighlight } from "#lib/utils/highlight.ts";
import { describe, expect, test } from "vitest";

describe("splitHighlight", () => {
  test("surligne chaque correspondance", () => {
    expect(splitHighlight("Saint-Malo", ["mal"])).toEqual([
      { text: "Saint-", match: false },
      { text: "Mal", match: true },
      { text: "o", match: false },
    ]);
  });

  test("applique tous les motifs en une passe", () => {
    expect(splitHighlight("Paris b", ["paris", "b"])).toEqual([
      { text: "Paris", match: true },
      { text: " ", match: false },
      { text: "b", match: true },
    ]);
  });

  test("préfère le motif le plus long", () => {
    expect(splitHighlight("Paris", ["par", "paris"])).toEqual([
      { text: "Paris", match: true },
    ]);
  });

  test("renvoie le texte entier sans motif", () => {
    expect(splitHighlight("<b>Paris</b>", [])).toEqual([
      { text: "<b>Paris</b>", match: false },
    ]);
  });
});
