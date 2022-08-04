import { describe, expect, test, it } from "vitest";
import { removeAllSpaces } from "../src/lib/schemas/utils.js";

describe("schema utils", () => {
  it("removeAllSpaces", () => {
    test("seulement des espaces", () => {
      expect(removeAllSpaces("")).toBe("");
      expect(removeAllSpaces(" ")).toBe("");
      expect(removeAllSpaces("  ")).toBe("");
    });

    test("Numéro de téléphone", () => {
      expect(removeAllSpaces("01 99 00 00 00")).toBe("0199000000");
    });
  });
});
