import { getApiURL } from "$lib/utils/api";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";

interface EmploisOrientationParams {
  serviceSlug: string;
  opJwt: string;
  token?: string;
}

export function handleEmploisOrientation({
  serviceSlug,
  opJwt,
  token,
}: EmploisOrientationParams) {
  const params = new URLSearchParams();
  params.set(ORIENTATION_JWT_QUERY_PARAM, opJwt);
  const apiUrl = `${getApiURL()}/orientations/emplois/${serviceSlug}/?${params}`;

  return fetch(apiUrl, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(token && { Authorization: `Token ${token}` }),
    },
  });
}
