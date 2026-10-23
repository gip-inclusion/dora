import { INCLUSION_PLATFORM_URL } from "$lib/env";
import type { Service } from "$lib/types";

const MATOMO_PARAMS = "mtm_campaign=DORA&mtm_kwd=orientation";

export function getPlateformeOrientationUrl(service: Service): string | null {
  if (!service.emploisUid) {
    return null;
  }

  const serviceId = encodeURIComponent(service.emploisUid);

  return `${INCLUSION_PLATFORM_URL}/insertion/orientations/${serviceId}/job-seeker/?${MATOMO_PARAMS}`;
}
