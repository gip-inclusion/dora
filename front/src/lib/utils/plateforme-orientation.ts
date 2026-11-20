import { INCLUSION_PLATFORM_URL } from "#lib/env.ts";
import type { Service } from "#lib/types.ts";

const MATOMO_PARAMS = "mtm_campaign=DORA&mtm_kwd=orientation";

// `emploisUid` est toujours renseigné pour un service (Dora ou data·inclusion)
export function getPlateformeOrientationUrl(service: Service): string {
  const serviceId = encodeURIComponent(service.emploisUid);

  return `${INCLUSION_PLATFORM_URL}/insertion/orientations/${serviceId}/job-seeker/?${MATOMO_PARAMS}`;
}
