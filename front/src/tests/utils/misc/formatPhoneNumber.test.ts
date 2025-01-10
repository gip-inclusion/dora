import { describe, expect, test } from "vitest";
import { formatPhoneNumber } from "$lib/utils/misc";

describe("formatPhoneNumber", () => {
  test("formate correctement un numéro de téléphone avec des espaces", () => {
    expect(formatPhoneNumber("06 12 34 56 78")).toBe("06 12 34 56 78");
  });

  test("supprime les espaces supplémentaires et formate correctement", () => {
    expect(formatPhoneNumber("06  12  34  56  78")).toBe("06 12 34 56 78");
  });

  test("gère un numéro sans espaces", () => {
    expect(formatPhoneNumber("0612345678")).toBe("06 12 34 56 78");
  });

  test("gère un numéro avec un nombre impair de chiffres", () => {
    expect(formatPhoneNumber("06123456789")).toBe("06 12 34 56 78 9");
  });

  test("retourne une chaîne vide pour une entrée vide", () => {
    expect(formatPhoneNumber("")).toBe("");
  });

  test("ignore les caractères non numériques", () => {
    expect(formatPhoneNumber("06a12b34c56d78")).toBe("06 12 34 56 78");
  });
});
