import { getApiURL } from "$lib/utils/api";

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
  const apiUrl = new URL(`/orientations/emplois/${serviceSlug}/`, getApiURL());
  apiUrl.searchParams.set("op", opJwt);

  return fetch(apiUrl, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      ...(token && { Authorization: `Token ${token}` }),
    },
  });
}
