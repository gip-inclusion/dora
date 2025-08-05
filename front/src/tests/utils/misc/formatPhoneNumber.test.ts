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

  test("convertit +33 en 0 pour les numéros français", () => {
    expect(formatPhoneNumber("+33 1 23 45 67 89")).toBe("01 23 45 67 89");
  });

  test("convertit +33 en 0 sans espaces", () => {
    expect(formatPhoneNumber("+33123456789")).toBe("01 23 45 67 89");
  });

  test("convertit +33 en 0 pour un numéro mobile", () => {
    expect(formatPhoneNumber("+33 6 12 34 56 78")).toBe("06 12 34 56 78");
  });

  test("garde le + pour les autres préfixes internationaux", () => {
    expect(formatPhoneNumber("+1 555 123 4567")).toBe("+155 51 23 45 67");
  });

  test("garde le + pour les autres préfixes sans espaces", () => {
    expect(formatPhoneNumber("+15551234567")).toBe("+155 51 23 45 67");
  });

  test("garde le + pour les préfixes européens", () => {
    expect(formatPhoneNumber("+44 20 7946 0958")).toBe("+442 07 94 60 95 8");
  });

  test("gère un numéro avec +33 et caractères non numériques", () => {
    expect(formatPhoneNumber("+33a1b2c3d4e5f6g7h8i9")).toBe("01 23 45 67 89");
  });
});
