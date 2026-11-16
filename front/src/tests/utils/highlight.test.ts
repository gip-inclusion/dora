import {
  buildHighlightPatterns,
  splitHighlight,
} from "#lib/utils/highlight.ts";
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

describe("buildHighlightPatterns", () => {
  test("échappe les caractères spéciaux, parenthèses comprises", () => {
    const patterns = buildHighlightPatterns("(a|b) c.", false);
    expect(splitHighlight("x (a|b) c.", patterns)).toEqual([
      { text: "x ", match: false },
      { text: "(a|b)", match: true },
      { text: " ", match: false },
      { text: "c.", match: true },
    ]);
  });

  test("ignore les accents si demandé", () => {
    const patterns = buildHighlightPatterns("evry  (", true);
    expect(splitHighlight("Évry (91)", patterns)).toEqual([
      { text: "Évry", match: true },
      { text: " ", match: false },
      { text: "(", match: true },
      { text: "91)", match: false },
    ]);
  });
});
