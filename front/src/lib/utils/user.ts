import { getApiURL } from "./api";
import type { DiscoveryMethod, UserMainActivity } from "./auth";

export interface UpdateUserProfileInput {
  mainActivity?: UserMainActivity;
  discoveryMethod?: DiscoveryMethod;
  discoveryMethodOther?: string;
}

export function updateUserProfile(userProfileData: UpdateUserProfileInput) {
  return fetch(`${getApiURL()}/profile/`, {
    method: "PATCH",
    body: JSON.stringify(userProfileData),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
    },
  });
}
