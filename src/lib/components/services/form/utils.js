import schema, { fields, fieldsRequired } from "$lib/schemas/service";
import { formatSchema } from "$lib/schemas/utils";

const serviceSchema = formatSchema(
  schema,
  fields.service,
  fieldsRequired.service
);

const defaultServiceCache = Object.fromEntries(
  Object.entries(serviceSchema).map(([fieldName, props]) => [
    fieldName,
    props.default,
  ])
);

export function getNewService() {
  return JSON.parse(JSON.stringify(defaultServiceCache));
}

const modelSchema = formatSchema(schema, fields.model, fieldsRequired.model);

const defaultModelCache = Object.fromEntries(
  Object.entries(modelSchema).map(([fieldName, props]) => [
    fieldName,
    props.default,
  ])
);

export function getNewModel() {
  return JSON.parse(JSON.stringify(defaultModelCache));
}
