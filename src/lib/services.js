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
  return (await fetchData(url)).data;
}

export async function getService(slug) {
  const url = `${getApiURL()}/services/${slug}/`;
  const data = (await fetchData(url)).data;
  if (data) {
    data.fullDesc = insane(markdownToHTML(data.fullDesc));
  }
  return data;
}

export async function createOrModifyService(service) {
  if (service.fullDesc) service.fullDesc = htmlToMarkdown(service.fullDesc);
  let method, url;
  if (service.slug) {
    url = `${getApiURL()}/services/${service.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/services/`;
    method = "POST";
  }

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(service),
  });

  const result = {
    ok: response.ok,
    status: response.status,
  };
  if (response.ok) {
    result.data = await response.json();
    if (result.data) {
      result.data.fullDesc = insane(markdownToHTML(result.data.fullDesc));
    }
  } else {
    try {
      result.error = await response.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

export async function publishDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ isDraft: false }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}

export async function getServicesOptions() {
  const url = `${getApiURL()}/services-options/`;
  return (await fetchData(url)).data;
}
