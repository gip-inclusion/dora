import { serviceSchema, modelSchema } from "$lib/schemas/service";

const defaultServiceCache = Object.fromEntries(
  Object.entries(serviceSchema).map(([fieldName, props]) => [
    fieldName,
    props.default,
  ])
);

export function getNewService() {
  return JSON.parse(JSON.stringify(defaultServiceCache));
}

const defaultModelCache = Object.fromEntries(
  Object.entries(modelSchema).map(([fieldName, props]) => [
    fieldName,
    props.default,
  ])
);

export function getNewModel() {
  return JSON.parse(JSON.stringify(defaultModelCache));
}

export function createModelFromService(service) {
  return JSON.parse(
    JSON.stringify(
      Object.fromEntries(
        Object.keys(modelSchema).map((fieldName) => [
          fieldName,
          service[fieldName],
        ])
      )
    )
  );
}
