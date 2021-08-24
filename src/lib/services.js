import insane from "insane";
import { get } from "svelte/store";
import { getApiURL, markdownToHTML, htmlToMarkdown } from "$lib/utils.js";
import { token } from "$lib/auth";

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
  const url = `${getApiURL()}/services/${slug}/`;
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

export async function createService(service) {
  if (service.fullDesc) service.fullDesc = htmlToMarkdown(service.fullDesc);
  const url = `${getApiURL()}/services/`;
  const method = "POST";

  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(service),
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

export async function modifyService(service) {
  if (service.fullDesc) service.fullDesc = htmlToMarkdown(service.fullDesc);
  const url = `${getApiURL()}/services/${service.slug}/`;

  const method = "PATCH";

  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",

      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(service),
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

export async function getServiceOptions() {
  const url = `${getApiURL()}/services/`;
  const res = await fetch(url, {
    method: "OPTIONS",
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (res.ok) {
    result.result = (await res.json()).actions.POST;
  } else {
    try {
      result.error = await res.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

export async function getPublicServicesOptions() {
  const url = `${getApiURL()}/services-options/`;

  const res = await fetch(url, {
    headers: {
      Accept: "application/json; version=1.0",
    },
  });
  if (res.ok) {
    const servicesOptions = await res.json();
    return {
      props: { servicesOptions },
    };
  }
  return {
    status: res.status,
    error: new Error(`Could not load ${url}`),
  };
}
