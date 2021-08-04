import { getApiURL } from "$lib/utils.js";

export async function getStructures() {
  const url = `${getApiURL()}/structures/`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    let structures = await res.json();
    return {
      props: { structures },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}
