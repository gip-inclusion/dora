import { beforeEach, describe, expect, test, vi } from "vitest";
import { isRedirect } from "@sveltejs/kit";
import type { Service } from "#lib/types.ts";
import { getService, getServiceDI } from "#lib/requests/services.ts";
import { isAuthenticated } from "#lib/utils/auth.ts";
import { load } from "../../routes/(modeles-services)/services/[slug]/orienter/+page";

vi.mock("#lib/utils/auth.ts", () => ({
  isAuthenticated: vi.fn(),
}));

vi.mock("#lib/requests/services.ts", () => ({
  getService: vi.fn(),
  getServiceDI: vi.fn(),
}));

// l'URL de La plateforme vient d'un `.env` non versionné : on la force pour
// que les tests ne dépendent pas de l'environnement
vi.mock("#lib/env.ts", () => ({
  INCLUSION_PLATFORM_URL: "https://plateforme.inclusion.gouv.fr",
}));

const EMPLOIS_UID = "dora--22e2a25c-ee9e-4606-9236-757417322c5b";
const PLATEFORME_URL = `https://plateforme.inclusion.gouv.fr/insertion/orientations/${EMPLOIS_UID}/job-seeker/?mtm_campaign=DORA&mtm_kwd=orientation`;

function makeService(overrides: Partial<Service> = {}): Service {
  return {
    slug: "un-service",
    isOrientable: true,
    coachOrientationModes: ["formulaire-dora"],
    emploisUid: EMPLOIS_UID,
    ...overrides,
  } as Service;
}

function callLoad(service: Service | null, slug = "un-service") {
  vi.mocked(getService).mockResolvedValue(service as Service);
  vi.mocked(getServiceDI).mockResolvedValue(service as never);
  return load({
    parent: () => Promise.resolve({}),
    params: { slug },
    fetch: vi.fn(),
    // lu par l'instrumentation Sentry qui enveloppe la fonction `load`
    url: new URL(`https://dora.fr/services/${slug}/orienter`),
  } as never);
}

async function captureRedirect(service: Service, slug?: string) {
  try {
    await callLoad(service, slug);
  } catch (err) {
    if (isRedirect(err)) {
      return err.location;
    }
    throw err;
  }
  throw new Error("aucune redirection déclenchée");
}

describe("page d’orientation", () => {
  beforeEach(() => {
    vi.mocked(isAuthenticated).mockReturnValue(false);
  });

  test("redirige l’utilisateur anonyme vers le formulaire de La plateforme", async () => {
    expect(await captureRedirect(makeService())).toEqual(PLATEFORME_URL);
  });

  test("redirige l’utilisateur connecté via l’auto-connexion Nexus", async () => {
    vi.mocked(isAuthenticated).mockReturnValue(true);

    expect(await captureRedirect(makeService())).toEqual(
      `/nexus/auto-login/?next=${encodeURIComponent(PLATEFORME_URL)}`
    );
  });

  test("refuse un service non orientable", async () => {
    await expect(
      callLoad(makeService({ isOrientable: false }))
    ).rejects.toThrow();
  });
  test("charge un service data·inclusion via son préfixe `di--`", async () => {
    const service = makeService({ emploisUid: "source--1234" });

    expect(await captureRedirect(service, "di--source--1234")).toContain(
      "/insertion/orientations/source--1234/job-seeker/"
    );
    expect(getServiceDI).toHaveBeenCalledWith(
      "source--1234",
      expect.anything()
    );
  });

  test("renvoie une 404 si le service est introuvable", async () => {
    await expect(callLoad(null)).rejects.toMatchObject({ status: 404 });
  });
});
