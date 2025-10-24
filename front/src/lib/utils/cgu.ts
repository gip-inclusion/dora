import { get } from "svelte/store";
import { token } from "./auth";
import { customFetch, getApiURL } from "./api";
import { CGU_VERSION } from "../../routes/(static)/cgu/version";

export function needToAcceptCgu(currentUserInfo) {
  return (
    CGU_VERSION &&
    !Object.keys(currentUserInfo.cguVersionsAccepted).includes(CGU_VERSION)
  );
}

export async function acceptCgu() {
  const url = `${getApiURL()}/auth/accept-cgu/`;
  const method = "POST";
  const response = await customFetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ cguVersion: CGU_VERSION }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}
