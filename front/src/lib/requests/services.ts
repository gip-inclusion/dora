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
  StructureService,
} from "$lib/types";
import {
  getCachedServicesOptions,
  setCachedServicesOptions,
} from "$lib/cache/services-options";
import { userInfo } from "$lib/utils/auth";
import { getAnalyticsId } from "$lib/utils/stats";
import { logException } from "$lib/utils/logger";

function serviceToBack(service) {
  if (service.longitude && service.latitude) {
    service.geom = {
      type: "Point",
      coordinates: [service.longitude, service.latitude],
    };
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

export async function getService(
  slug: string,
  fetch = window.fetch
): Promise<Service> {
  const url = `${getApiURL()}/services/${slug}/`;
  const response = await fetchData<Service>(url, fetch);

  if (!response.data) {
    return null;
  }
  // TODO: 404

  return serviceToFront(response.data);
}

export async function getServiceDI(
  diId: string,
  fetch = window.fetch
): Promise<Service> {
  const userHash = getAnalyticsId();
  const url = new URL(`/services-di/${diId}/`, getApiURL());

  const response = await fetchData<Service>(
    url.toString(),
    fetch,
    userHash
      ? {
          "Anonymous-User-Hash": userHash,
        }
      : {}
  );

  if (!response.data) {
    return null;
  }
  // TODO: 404

  return serviceToFront(response.data);
}

export async function getPublishedServices({
  pageSize,
  page,
}: {
  pageSize: number;
  page: number;
}) {
  const url = new URL("/services/", getApiURL());

  url.searchParams.append("published", "1");
  url.searchParams.append("page_size", pageSize.toString());
  url.searchParams.append("page", page.toString());

  return (
    await fetchData<{ count: number; results: ShortService[] }>(url.toString())
  ).data;
}

export async function getModel(slug, fetch = window.fetch): Promise<Model> {
  const url = `${getApiURL()}/models/${slug}/`;
  const response = await fetchData<Model>(url, fetch);

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

export function markServiceAsSynced(service: Service | ShortService) {
  return fetch(`${getApiURL()}/services/${service.slug}/`, {
    method: "PATCH",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ markSynced: true }),
  });
}

export async function createOrModifyModel(model, updateAllServices = false) {
  let method, url;
  if (model.slug) {
    url = `${getApiURL()}/models/${model.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/models/`;
    method = "POST";
  }

  let data = { ...serviceToBack(model) };
  if (updateAllServices) {
    data = { ...data, updateAllServices };
  }

  const result = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(data),
  });

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

export async function getBookmarks(
  fetch = window.fetch
): Promise<ShortService[]> {
  const url = `${getApiURL()}/bookmarks/`;
  return (await fetchData<ShortService[]>(url, fetch)).data;
}

export async function setBookmark(bookmarkSlug: string, isDI: boolean) {
  const url = `${getApiURL()}/bookmarks/`;
  const method = "POST";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({ slug: bookmarkSlug, isDI }),
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
}

export async function clearBookmark(bookmarkId: number) {
  const url = `${getApiURL()}/bookmarks/${bookmarkId}/`;
  const method = "DELETE";
  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
  });
  if (!response.ok) {
    throw Error(response.statusText);
  }
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

export async function getServicesOptions(
  fetch = window.fetch,
  useCache = true
): Promise<ServicesOptions> {
  const currentUserInfo = get(userInfo);

  if (useCache) {
    // Retourne les données du cache s'il existe et est valide
    const cached = getCachedServicesOptions(currentUserInfo);
    if (cached) {
      return cached;
    }
  }

  // Si pas de cache valide ou si le cache n'est pas utilisé, on fait l'appel API
  const url = `${getApiURL()}/services-options/`;
  const response = await fetchData<ServicesOptions>(url, fetch);
  if (!response.data) {
    throw Error(response.statusText);
  }

  // On met en cache les nouvelles données avec le contexte utilisateur actuel
  setCachedServicesOptions(response.data, currentUserInfo);

  return response.data;
}

export function updateServicesFromModel(
  services: Service[] | StructureService[]
) {
  return fetch(`${getApiURL()}/services/update-from-model/`, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({
      services: services.map((serv) => serv.slug),
    }),
  });
}

type ModelToService = {
  modelSlug: string;
  serviceSlug: string;
};

export function addIgnoredServicesToUpdate(
  modelToServiceSlugs: ModelToService[]
) {
  return fetch(`${getApiURL()}/services/reject-update-from-model/`, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({
      data: modelToServiceSlugs,
    }),
  });
}

export function markServicesAsUpToDate(services: { slug: string }[]) {
  return fetch(`${getApiURL()}/services/mark-as-up-to-date/`, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify({
      services: services.map((serv) => serv.slug),
    }),
  });
}
