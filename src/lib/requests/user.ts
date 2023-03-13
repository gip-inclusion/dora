import { getApiURL } from "$lib/utils/api";
import { get } from "svelte/store";
import { token } from "$lib/utils/auth";

export function setUserHasDoneASearch(): Promise<Response> {
  const url = `${getApiURL()}/profile/change/`;
  return fetch(url, {
    method: "POST",
    body: JSON.stringify({
      onboardingActionsAccomplished: {
        hasDoneASearch: true,
      },
    }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });
}
