import { error } from "@sveltejs/kit";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";
import {
  getOrientationBeneficiaryInfo,
  type OrientationBeneficiaryInfo,
} from "$lib/requests/nexus";

export const load = async ({ parent, url }) => {
  const data = await parent();
  const { service } = data;

  // on ne doit pas pouvoir accèder à cette page
  // si le service n'est pas orientable ou si le
  // formulaire DORA n'est pas un mode d'orientation
  if (
    (!service.isOrientable ||
      !service.coachOrientationModes?.includes("formulaire-dora")) &&
    !service.isOrientableFtService
  ) {
    error(400, "Service non-orientable");
  }

  let beneficiaryInfo: OrientationBeneficiaryInfo | null = null;
  const opJwt = url.searchParams.get(ORIENTATION_JWT_QUERY_PARAM);
  if (opJwt) {
    try {
      beneficiaryInfo = await getOrientationBeneficiaryInfo(opJwt);
    } catch {
      beneficiaryInfo = null;
    }
  }

  return {
    ...data,
    beneficiaryInfo,
  };
};
