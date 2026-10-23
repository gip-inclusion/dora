import { describe, expect, test } from "vitest";
import type { Service } from "#lib/types.ts";
import { getPlateformeOrientationUrl } from "#lib/utils/plateforme-orientation.ts";

function makeService(emploisUid: string | undefined): Service {
  return { emploisUid } as Service;
}

describe("getPlateformeOrientationUrl", () => {
  test("construit l’URL du formulaire d’orientation pour un service Dora", () => {
    const service = makeService("dora--22e2a25c-ee9e-4606-9236-757417322c5b");

    expect(getPlateformeOrientationUrl(service)).toEqual(
      "https://plateforme.inclusion.gouv.fr/insertion/orientations/dora--22e2a25c-ee9e-4606-9236-757417322c5b/job-seeker/?mtm_campaign=DORA&mtm_kwd=orientation"
    );
  });

  test("construit l’URL avec l’identifiant d’un service data·inclusion", () => {
    const service = makeService("monenfant--1234");

    expect(getPlateformeOrientationUrl(service)).toEqual(
      "https://plateforme.inclusion.gouv.fr/insertion/orientations/monenfant--1234/job-seeker/?mtm_campaign=DORA&mtm_kwd=orientation"
    );
  });

  test("encode l’identifiant dans le chemin", () => {
    const service = makeService("source avec espace--1/2");

    expect(getPlateformeOrientationUrl(service)).toContain(
      "/insertion/orientations/source%20avec%20espace--1%2F2/job-seeker/"
    );
  });

  test("renvoie null quand le service n’a pas d’identifiant Emplois", () => {
    expect(getPlateformeOrientationUrl(makeService(undefined))).toBeNull();
    expect(getPlateformeOrientationUrl(makeService(""))).toBeNull();
  });
});
