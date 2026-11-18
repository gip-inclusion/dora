import { error, redirect } from "@sveltejs/kit";
import type { Service } from "#lib/types.ts";
import { getService, getServiceDI } from "#lib/requests/services.ts";
import { isAuthenticated } from "#lib/utils/auth.ts";
import { generateOutboundNexusAutoLoginUrl } from "#lib/utils/nexus.ts";
import { getPlateformeOrientationUrl } from "#lib/utils/plateforme-orientation.ts";
import { INCLUSION_PLATFORM_URL } from "#lib/env.ts";
import type { PageLoad } from "./$types";

export const ssr = false;

// L'orientation se fait sur La plateforme de l'inclusion : cette page ne fait
// que rediriger, elle reste exposée car l'API data·inclusion publie son URL
// (`formulaire_en_ligne`).
export const load: PageLoad = async ({ fetch, params, parent }) => {
  await parent();

  const service = params.slug.startsWith("di--")
    ? ((await getServiceDI(params.slug.slice(4), fetch)) as Service)
    : await getService(params.slug, fetch);

  if (!service) {
    error(404, "Page Not Found");
  }

  if (
    !service.isOrientable ||
    !service.coachOrientationModes?.includes("formulaire-dora")
  ) {
    error(400, "Service non-orientable");
  }

  const plateformeUrl = getPlateformeOrientationUrl(service);

  // les utilisateurs connectés passent par l'auto-connexion Nexus, qui les
  // dépose authentifiés sur le formulaire s'ils ont un compte plateforme
  redirect(
    302,
    isAuthenticated()
      ? generateOutboundNexusAutoLoginUrl(plateformeUrl)
      : plateformeUrl,
    { external: [INCLUSION_PLATFORM_URL] }
  );
};
