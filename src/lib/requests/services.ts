import { getApiURL } from "$lib/utils/api";
import { token } from "$lib/utils/auth";
import { fetchData } from "$lib/utils/misc";
import { get } from "svelte/store";
import type {
  Model,
  Service,
  ServicesOptions,
  ServiceStatus,
  ShortService,
} from "$lib/types";
import { logException } from "$lib/utils/logger";

function serviceToBack(service) {
  if (service.longitude && service.latitude) {
    service.geom = {
      type: "Point",
      coordinates: [service.longitude, service.latitude],
    };
  } else {
    service.geom = null;
  }

  return service;
}

function serviceToFront(service) {
  let lng, lat;
  if (service.geom) {
    [lng, lat] = service.geom.coordinates;
  }
  service.longitude = lng;
  service.latitude = lat;

  return service;
}

export async function getService(slug): Promise<Service> {
  const url = `${getApiURL()}/services/${slug}/`;
  const response = await fetchData<Service>(url);

  if (!response.data) {
    return null;
  }
  // TODO: 404

  return serviceToFront(response.data);
}

export async function getPublishedServices(): Promise<ShortService[]> {
  const url = `${getApiURL()}/services/?published=1`;
  return (await fetchData<ShortService[]>(url)).data;
}

export async function getModel(slug): Promise<Model> {
  const url = `${getApiURL()}/models/${slug}/`;
  const response = await fetchData<Model>(url);

  if (!response.data) {
    return null;
  }
  // TODO: 404

  return serviceToFront(response.data);
}

export function createOrModifyService(service: Service) {
  let method, url;
  if (service.slug) {
    url = `${getApiURL()}/services/${service.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/services/`;
    method = "POST";
  }

  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(serviceToBack(service)),
  });
}

export function createOrModifyModel(model) {
  let method, url;
  if (model.slug) {
    url = `${getApiURL()}/models/${model.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/models/`;
    method = "POST";
  }

  return fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(serviceToBack(model)),
  });
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

export async function setBookmark(serviceSlug: string, wantedState: boolean) {
  const url = `${getApiURL()}/services/${serviceSlug}/set-bookmark/`;
  const method = "POST";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ state: wantedState }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function publishDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "PUBLISHED";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    throw Error(response.statusText);
  }

  return response.json();
}

export async function unPublishService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "DRAFT";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

export async function archiveService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "ARCHIVED";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

export async function unarchiveService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "DRAFT";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

export async function publishService(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "PUBLISHED";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

export async function convertSuggestionToDraft(serviceSlug) {
  const url = `${getApiURL()}/services/${serviceSlug}/`;
  const method = "PATCH";
  const status: ServiceStatus = "DRAFT";

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ status }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response.json();
}

export async function getServicesOptions(): Promise<ServicesOptions | null> {
  const url = `${getApiURL()}/services-options/`;
  return (await fetchData<ServicesOptions>(url)).data;
}
