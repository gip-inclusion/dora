import { browser } from "$app/env";

import serviceSchema from "$lib/schemas/service";
import { storageKey } from "./_constants";

const defaultServiceCache = Object.fromEntries(
  Object.entries(serviceSchema).map(([fieldName, props]) => [
    fieldName,
    props.default,
  ])
);

export function resetServiceCache() {
  localStorage.removeItem(storageKey);
}

export function persistServiceCache(service) {
  localStorage.setItem(storageKey, JSON.stringify(service));
}

export function getNewService() {
  if (browser) {
    const lsContent = localStorage.getItem(storageKey);
    if (lsContent) {
      return JSON.parse(lsContent);
    }
  }
  return JSON.parse(JSON.stringify(defaultServiceCache));
}
