import { describe, expect, it } from "vitest";

import { buildMobilizationModes } from "$lib/utils/service-share-mailto";

describe("buildMobilizationModes", () => {
  it("retourne les libellés des modes de mobilisation", () => {
    expect(
      buildMobilizationModes(["Envoyer un courriel", "Téléphoner"], "")
    ).toEqual(["Envoyer un courriel", "Téléphoner"]);
  });

  it("ajoute les précisions à la suite des modes", () => {
    expect(
      buildMobilizationModes(["Téléphoner"], "Uniquement le mardi matin")
    ).toEqual(["Téléphoner", "Uniquement le mardi matin"]);
  });

  it("ignore des précisions vides ou blanches", () => {
    expect(buildMobilizationModes(["Téléphoner"], "   ")).toEqual([
      "Téléphoner",
    ]);
  });

  it("accepte l'absence de modes", () => {
    expect(buildMobilizationModes(null, "Nous consulter")).toEqual([
      "Nous consulter",
    ]);
    expect(buildMobilizationModes(undefined, null)).toEqual([]);
  });
});
