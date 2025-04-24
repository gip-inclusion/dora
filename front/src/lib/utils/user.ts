import { get } from "svelte/store";
import { API_URL } from "$lib/env";
import { token, type DiscoveryMethod, type UserMainActivity } from "./auth";

export interface UpdateUserProfileInput {
  mainActivity?: UserMainActivity;
  discoveryMethod?: DiscoveryMethod;
  discoveryMethodOther?: string;
}

export function updateUserProfile(userProfileData: UpdateUserProfileInput) {
  return fetch(`${API_URL}/profile/`, {
    method: "PATCH",
    body: JSON.stringify(userProfileData),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });
}
