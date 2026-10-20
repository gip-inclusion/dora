import { afterEach, describe, expect, test, vi } from "vitest";
import { isHttpError, isRedirect } from "@sveltejs/kit";
import { load } from "../../routes/nexus/auto-login/+page.server";

const PLATEFORME_URL =
  "https://plateforme.inclusion.gouv.fr/insertion/orientations/dora--1234/job-seeker/?mtm_campaign=DORA";

function callLoad(next: string | null, token: string | null = "un-token") {
  const url = new URL("https://dora.fr/nexus/auto-login/");
  if (next !== null) {
    url.searchParams.set("next", next);
  }
  return load({
    cookies: { get: () => token ?? undefined },
    url,
    // le wrapper Sentry a besoin de ces propriétés de l'événement
    request: new Request(url),
    route: { id: "/nexus/auto-login" },
  } as never);
}

async function capture(next: string | null, token: string | null = "un-token") {
  try {
    await callLoad(next, token);
  } catch (err) {
    if (isRedirect(err)) {
      return { location: err.location };
    }
    if (isHttpError(err)) {
      return { status: err.status };
    }
    throw err;
  }
  throw new Error("ni redirection ni erreur");
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("auto-connexion Nexus sortante", () => {
  test("redirige vers l’URL d’auto-connexion renvoyée par l’API", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({ redirectUrl: `${PLATEFORME_URL}&auto_login=jwt` }),
      })
    );

    expect(await capture(PLATEFORME_URL)).toEqual({
      location: `${PLATEFORME_URL}&auto_login=jwt`,
    });
  });

  test("redirige quand même vers La plateforme si l’auto-connexion échoue", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

    expect(await capture(PLATEFORME_URL)).toEqual({ location: PLATEFORME_URL });
  });

  test("redirige quand même vers La plateforme si l’API est injoignable", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("fetch failed"))
    );

    expect(await capture(PLATEFORME_URL)).toEqual({ location: PLATEFORME_URL });
  });

  test("redirige vers La plateforme si la réponse de l’API est illisible", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.reject(new SyntaxError("Unexpected token")),
      })
    );

    expect(await capture(PLATEFORME_URL)).toEqual({ location: PLATEFORME_URL });
  });

  test("redirige vers La plateforme si l’utilisateur n’a pas de session Dora", async () => {
    expect(await capture(PLATEFORME_URL, null)).toEqual({
      location: PLATEFORME_URL,
    });
  });

  test("ne redirige pas vers un domaine tiers", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

    expect(await capture("https://exemple-malveillant.fr/phishing")).toEqual({
      status: 404,
    });
  });

  // ces deux URL commencent par l'URL de La plateforme : un contrôle par préfixe
  // de chaîne les accepterait, d'où la comparaison des origins
  test("ne redirige pas vers un domaine suffixé", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

    expect(
      await capture(
        "https://plateforme.inclusion.gouv.fr.exemple-malveillant.fr/phishing"
      )
    ).toEqual({ status: 404 });
  });

  test("ne redirige pas vers un hôte masqué par des identifiants", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));

    expect(
      await capture(
        "https://plateforme.inclusion.gouv.fr@exemple-malveillant.fr/phishing"
      )
    ).toEqual({ status: 404 });
  });

  test("renvoie une 404 sans paramètre `next`", async () => {
    expect(await capture(null)).toEqual({ status: 404 });
  });
});
