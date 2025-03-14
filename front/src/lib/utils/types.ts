import type { Model, Service } from "$lib/types";

export function isModel(service: Service | Model): service is Model {
  return "source" in service;
}

export function isService(service: Service | Model): service is Service {
  return !isModel(service);
}
