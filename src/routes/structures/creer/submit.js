import { get } from "svelte/store";

import { getApiURL } from "$lib/utils";
import { token } from "$lib/auth";

export async function submit(structure) {
  const url = `${getApiURL()}/structures/`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(structure),
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (res.ok) {
    result.result = await res.json();
  } else {
    try {
      result.error = await res.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}
