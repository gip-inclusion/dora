import { error, redirect } from "@sveltejs/kit";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";
import {
  getOrientationBeneficiaryInfo,
  type OrientationBeneficiaryInfo,
} from "$lib/requests/nexus";
import { isAuthenticated } from "$lib/utils/auth";
import { transferUrlParams } from "$lib/utils/misc";
import { generateOutboundNexusAutoLoginUrl } from "$lib/utils/nexus";
import { getPlateformeOrientationUrl } from "$lib/utils/plateforme-orientation";
import { ORIENTATION_REDIRECTION_FEATURE_FLAG } from "$lib/env";

export const load = async ({ parent, url, params, fetch }) => {
  const data = await parent();
  const { service } = data;

  // on ne doit pas pouvoir accèder à cette page
  // si le service n'est pas orientable ou si le
  // formulaire DORA n'est pas un mode d'orientation
  if (
    !service.isOrientable ||
    !service.coachOrientationModes.includes("formulaire-dora")
  ) {
    error(400, "Service non-orientable");
  }

  let beneficiaryInfo: OrientationBeneficiaryInfo | null = null;
  const opJwt = url.searchParams.get(ORIENTATION_JWT_QUERY_PARAM);
  if (opJwt) {
    try {
      beneficiaryInfo = await getOrientationBeneficiaryInfo(
        opJwt,
        params.slug,
        fetch
      );
    } catch {
      beneficiaryInfo = null;
    }
    if (beneficiaryInfo && "nextUrl" in beneficiaryInfo) {
      redirect(
        302,
        transferUrlParams({
          targetUrl: beneficiaryInfo.nextUrl,
          sourceUrl: url,
          exclude: [ORIENTATION_JWT_QUERY_PARAM],
        })
      );
    }
  } else if (ORIENTATION_REDIRECTION_FEATURE_FLAG) {
    // l'orientation se fait désormais sur La plateforme de l'inclusion ;
    // le formulaire Dora n'est conservé que pour les orientations initiées
    // depuis Les Emplois (`op`), en cours de retrait, et en dernier recours
    // si le service n'a pas d'identifiant côté plateforme.
    const plateformeUrl = getPlateformeOrientationUrl(service);
    if (plateformeUrl) {
      // les utilisateurs connectés passent par l'auto-connexion Nexus, qui les
      // dépose authentifiés sur le formulaire s'ils ont un compte plateforme
      redirect(
        302,
        isAuthenticated()
          ? generateOutboundNexusAutoLoginUrl(plateformeUrl)
          : plateformeUrl
      );
    }
  }

  return {
    ...data,
    beneficiaryInfo,
  };
};
