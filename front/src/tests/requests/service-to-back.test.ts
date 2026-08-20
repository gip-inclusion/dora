import { describe, expect, test } from "vitest";
import { serviceToBack } from "$lib/requests/services";

describe("serviceToBack", () => {
  test("n’envoie pas l’alias de compatibilité de la description", () => {
    const payload = serviceToBack({
      description: "Description modifiée",
      fullDesc: "Description chargée",
    });

    expect(payload).toEqual({ description: "Description modifiée" });
  });
});
