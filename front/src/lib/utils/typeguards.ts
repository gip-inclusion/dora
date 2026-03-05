import type { Model, Service } from "$lib/types";

export function isModel(
  serviceOrModel: Service | Model
): serviceOrModel is Model {
  return serviceOrModel.isModel;
}

export function isService(
  serviceOrModel: Service | Model
): serviceOrModel is Service {
  return !isModel(serviceOrModel);
}
