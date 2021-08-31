import insane from "insane";
import { get } from "svelte/store";
import {
  getApiURL,
  markdownToHTML,
  htmlToMarkdown,
  fetchData,
} from "$lib/utils.js";
import { token } from "$lib/auth";

export async function getServices() {
  const url = `${getApiURL()}/services/`;
  return await fetchData(url);
}

export async function getService(slug) {
  const url = `${getApiURL()}/services/${slug}/`;
  const result = await fetchData(url);
  if (result.data) {
    result.data.fullDesc = insane(markdownToHTML(result.data.fullDesc));
  }
  return result;
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

export async function getServicesOptions() {
  const url = `${getApiURL()}/services-options/`;
  return await fetchData(url);
}
