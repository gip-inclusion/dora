import { describe, expect, test } from "vitest";
import { getFileNameFromPath } from "$lib/utils/file";

describe("getFileNameFromPath", () => {
  test("renvoie le nom de fichier d’une clé de stockage", () => {
    expect(getFileNameFromPath("prod/42/dossier.pdf")).toBe("dossier.pdf");
  });

  test("renvoie la valeur telle quelle en l’absence de chemin", () => {
    expect(getFileNameFromPath("dossier.pdf")).toBe("dossier.pdf");
  });

  test("renvoie une chaîne vide pour un chemin vide", () => {
    expect(getFileNameFromPath("")).toBe("");
  });
});
