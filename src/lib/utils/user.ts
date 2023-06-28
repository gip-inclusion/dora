import { get } from "svelte/store";
import { getApiURL } from "./api";
import { token, type UserMainActivity } from "./auth";

export function updateUserMainActivity(userMainActivity: UserMainActivity) {
  return fetch(`${getApiURL()}/profile/main-activity/`, {
    method: "POST",
    body: JSON.stringify({ mainActivity: userMainActivity }),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });
}
