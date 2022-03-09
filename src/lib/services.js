import insane from "insane";
import { get } from "svelte/store";

import { markdownToHTML, htmlToMarkdown, fetchData } from "$lib/utils.js";
import { getApiURL } from "$lib/utils/api.js";
import { token } from "$lib/auth";
import { logException } from "./logger";

function serviceToBack(service) {
  if (service.fullDesc) service.fullDesc = htmlToMarkdown(service.fullDesc);
  if (service.longitude && service.latitude) {
    service.geom = {
      type: "Point",
      coordinates: [service.longitude, service.latitude],
    };
  } else {
    service.geom = null;
  }
  // Dans le futur, un service pourra appartenir à plusieurs categories
  // Le back-end le gère déjà, mais pour le moment on reste sur une categorie ici
  service.categories = [service.category];
  return service;
}

function serviceToFront(service) {
  if (service.fullDesc)
    service.fullDesc = insane(markdownToHTML(service.fullDesc), {
      allowedAttributes: { a: ["class", "rel", "href"] },
    });
  let lng, lat;
  if (service.geom) {
    [lng, lat] = service.geom.coordinates;
  }
  service.longitude = lng;
  service.latitude = lat;
  // Dans le futur, un service pourra appartenir à plusieurs categories
  // Le back-end le gère déjà, mais pour le moment on reste sur une categorie ici
  service.category = service.categories?.[0];
  service.categoryDisplay = service.categoriesDisplay?.[0];
  return service;
}

function serviceSuggestiontoBack(serviceSuggestion) {
  if (serviceSuggestion.fullDesc)
    serviceSuggestion.fullDesc = htmlToMarkdown(serviceSuggestion.fullDesc);

  // Dans le futur, un service pourra appartenir à plusieurs categories
  // Le back-end le gère déjà, mais pour le moment on reste sur une categorie ici
  serviceSuggestion.categories = [serviceSuggestion.category];
  return serviceSuggestion;
}

function serviceSuggestionToFront(serviceSuggestion) {
  const serviceInfo = serviceSuggestion.serviceInfo;
  if (serviceInfo.fullDesc)
    serviceInfo.fullDesc = insane(markdownToHTML(serviceInfo.fullDesc), {
      allowedAttributes: { a: ["class", "rel", "href"] },
    });
  // Dans le futur, un service pourra appartenir à plusieurs categories
  // Le back-end le gère déjà, mais pour le moment on reste sur une categorie ici
  serviceInfo.category = serviceInfo.categories?.[0];
  serviceInfo.categoryDisplay = serviceInfo.categoriesDisplay?.[0];
  return serviceSuggestion;
}

export async function getServices() {
  const url = `${getApiURL()}/services/`;
  return (await fetchData(url)).data;
}

export async function getMyServices() {
  const url = `${getApiURL()}/services/?mine=1`;
  return (await fetchData(url)).data;
}

export async function getService(slug) {
  const url = `${getApiURL()}/services/${slug}/`;
  const data = (await fetchData(url)).data;
  if (data) return serviceToFront(data);
  // TODO: 404
  return null;
}

export async function createOrModifyService(service) {
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
    body: JSON.stringify(serviceToBack(service)),
  });

  const result = {
    ok: response.ok,
    status: response.status,
  };
  if (response.ok) {
    result.data = serviceToFront(await response.json());
  } else {
    try {
      result.error = await response.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}

export async function deleteService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "DELETE";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (!res.ok) {
    try {
      result.error = await res.json();
    } catch (err) {
      logException(err);
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

export async function unPublishService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ isDraft: true }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}

export async function convertSuggestionToDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ isDraft: true, isSuggestion: false }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return await response.json();
}

export async function getLastDraft() {
  if (token) {
    const url = `${getApiURL()}/services/last-draft/`;
    return (await fetchData(url)).data;
  }
  return null;
}

export async function getServicesOptions({ kitFetch } = {}) {
  const url = `${getApiURL()}/services-options/`;
  try {
    return (await fetchData(url, { kitFetch })).data;
  } catch (err) {
    logException(err);
    return {};
  }
}

export async function getServiceSuggestions() {
  const url = `${getApiURL()}/services-suggestions/`;
  const results = (await fetchData(url)).data;
  if (results) return results.map((s) => serviceSuggestionToFront(s));
  return [];
}

export async function deleteServiceSuggestion(suggestion) {
  const url = `${getApiURL()}/services-suggestions/${suggestion.id}/`;
  const method = "DELETE";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (!res.ok) {
    try {
      result.error = await res.json();
    } catch (err) {
      logException(err);
    }
  }
  return result;
}

export async function acceptServiceSuggestion(suggestion) {
  const url = `${getApiURL()}/services-suggestions/${suggestion.id}/validate/`;
  const method = "POST";
  const res = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${get(token)}`,
    },
  });

  const result = {
    ok: res.ok,
    status: res.status,
  };
  if (!res.ok) {
    try {
      result.error = await res.json();
    } catch (err) {
      logException(err);
    }
  }
  return result;
}

export async function publishServiceSuggestion(suggestion) {
  const url = `${getApiURL()}/services-suggestions/`;
  const method = "POST";
  const { siret, name, ...contents } = serviceSuggestiontoBack(suggestion);
  const authToken = get(token);
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: authToken ? `Token ${get(token)}` : undefined,
    },
    body: JSON.stringify({
      siret,
      name,
      contents,
    }),
  });

  const result = {
    ok: response.ok,
    status: response.status,
  };
  if (response.ok) {
    result.data = await response.json();
  } else {
    try {
      result.error = await response.json();
    } catch (err) {
      console.error(err);
    }
  }
  return result;
}
