import { getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { get } from "svelte/store";
import hexoid from "hexoid";

const analyticsIdKey = "userHash";
function getAnalyticsId() {
  let analyticsId = localStorage.getItem(analyticsIdKey);
  if (!analyticsId) {
    analyticsId = hexoid(32)();
    localStorage.setItem(analyticsIdKey, analyticsId);
  }
  return analyticsId;
}

export function logAnalyticsEvent(tag, path, params = {}) {
  const data = {
    tag,
    path,
    userHash: getAnalyticsId(),
    ...params,
  };
  const currentToken = get(token);

  return fetch(`${getApiURL()}/stats/event/`, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: currentToken ? `Token ${currentToken}` : undefined,
    },
    body: JSON.stringify(data),
  });
}
