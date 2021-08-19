import insane from "insane";

import { getApiURL, markdownToHTML } from "$lib/utils.js";

export async function getServices() {
  const url = `${getApiURL()}/services/`;
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    const services = await res.json();
    return {
      props: { services },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}

export async function getService(slug) {
  console.log(slug);
  const url = `${getApiURL()}/services/${slug}/`;
  console.log(url);
  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });

  if (res.ok) {
    const service = await res.json();
    service.fullDesc = insane(markdownToHTML(service.fullDesc));
    return {
      props: { service },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}
