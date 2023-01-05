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
} from "../types";
import { logException } from "../utils/logger";

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

export async function getMyServices(): Promise<ShortService[]> {
  const url = `${getApiURL()}/services/?mine=1`;
  return (await fetchData<ShortService[]>(url)).data;
}

export async function getService(slug): Promise<Service> {
  const url = `${getApiURL()}/services/${slug}/`;
  const response = await fetchData<Service>(url);

  if (!response.data) return null;
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

  if (!response.data) return null;
  // TODO: 404

  return serviceToFront(response.data);
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

export async function createOrModifyModel(model) {
  let method, url;
  if (model.slug) {
    url = `${getApiURL()}/models/${model.slug}/`;
    method = "PATCH";
  } else {
    url = `${getApiURL()}/models/`;
    method = "POST";
  }

  const response = await fetch(url, {
    method,
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
      Authorization: `Token ${get(token)}`,
    },
    body: JSON.stringify(serviceToBack(model)),
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

  return await response.json();
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
  return await response.json();
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
  return await response.json();
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
  return await response.json();
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
  return await response.json();
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
  return await response.json();
}

export async function getLastDraft(): Promise<Service> {
  if (token) {
    const url = `${getApiURL()}/services/last-draft/`;
    return (await fetchData<Service>(url)).data;
  }
  return null;
}

let servicesOptionsBase;
export async function getServicesOptions({
  model = null,
} = {}): Promise<ServicesOptions> {
  if (!servicesOptionsBase) {
    const url = `${getApiURL()}/services-options/`;
    try {
      servicesOptionsBase = (await fetchData<ServicesOptions>(url)).data;
    } catch (err) {
      logException(err);
      return {};
    }
  }

  const data = { ...servicesOptionsBase };
  if (model?.customizableChoicesSet) {
    for (const field of [
      "accessConditions",
      "concernedPublic",
      "requirements",
      "credentials",
    ]) {
      data[field] = data[field].filter((option) =>
        model.customizableChoicesSet[field].includes(option.value)
      );
    }
  }

  return data;
}

export async function getServiceSuggestions() {
  const url = `${getApiURL()}/services-suggestions/`;
  const results = (await fetchData(url)).data;
  if (!results) return [];

  return results;
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
  } else {
    try {
      result.data = await res.json();
    } catch (err) {
      logException(err);
    }
  }
  return result;
}

export async function publishServiceSuggestion(suggestion, source) {
  const url = `${getApiURL()}/services-suggestions/`;
  const method = "POST";
  const { siret, name, ...contents } = suggestion;
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
      source,
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
