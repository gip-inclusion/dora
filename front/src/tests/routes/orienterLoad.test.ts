import { beforeEach, describe, expect, test, vi } from "vitest";
import { isRedirect } from "@sveltejs/kit";
import type { Service } from "$lib/types";
import { isAuthenticated } from "$lib/utils/auth";
import { load } from "../../routes/(modeles-services)/services/[slug]/orienter/+page";

vi.mock("$lib/utils/auth", () => ({
  isAuthenticated: vi.fn(),
}));

// la redirection est derrière un feature flag, alimenté par un `.env` non
// versionné : on le force pour que les tests ne dépendent pas de l'environnement
vi.mock("$lib/env", () => ({
  INCLUSION_PLATFORM_URL: "https://plateforme.inclusion.gouv.fr",
  ORIENTATION_REDIRECTION_FEATURE_FLAG: true,
}));

vi.mock("$lib/requests/nexus", () => ({
  getOrientationBeneficiaryInfo: vi.fn(),
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

function callLoad(service: Service, search = "") {
  return load({
    parent: () => Promise.resolve({ service }),
    url: new URL(`https://dora.fr/services/${service.slug}/orienter${search}`),
    params: { slug: service.slug },
    fetch: vi.fn(),
  } as never);
}

async function captureRedirect(service: Service, search = "") {
  try {
    await callLoad(service, search);
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

  test("conserve le formulaire Dora si le service n’a pas d’identifiant Emplois", async () => {
    const service = makeService({ emploisUid: undefined });

    const result = await callLoad(service);

    expect(result.service).toBe(service);
  });

  test("refuse un service non orientable", async () => {
    await expect(
      callLoad(makeService({ isOrientable: false }))
    ).rejects.toThrow();
  });
});
