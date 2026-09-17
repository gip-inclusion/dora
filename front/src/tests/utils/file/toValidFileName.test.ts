import { describe, expect, test } from "vitest";
import { toValidFileName } from "$lib/utils/file";

// Les cas attendus sont ceux de `django.utils.text.get_valid_filename`, appliqué par le
// serveur avant de stocker le document.
describe("toValidFileName", () => {
  test("laisse un nom déjà valide intact", () => {
    expect(toValidFileName("dossier.pdf")).toBe("dossier.pdf");
  });

  test("remplace les espaces par des tirets bas", () => {
    expect(toValidFileName("mon dossier.pdf")).toBe("mon_dossier.pdf");
  });

  test("supprime les caractères non autorisés", () => {
    expect(toValidFileName("Fiche d'inscription (2024).pdf")).toBe(
      "Fiche_dinscription_2024.pdf"
    );
  });

  test("conserve les caractères accentués", () => {
    expect(toValidFileName("dossier école.pdf")).toBe("dossier_école.pdf");
  });

  test("ignore les espaces de début et de fin", () => {
    expect(toValidFileName("  dossier.pdf  ")).toBe("dossier.pdf");
  });
});
