import type { Model, Service, ServicesOptions } from "$lib/types";
import type { Schema } from "$lib/validation/schema-utils";
import { modelSchema, serviceSchema } from "$lib/validation/schemas/service";

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

// Champs dont les choix sont exposés dans `servicesOptions` sous une clé au pluriel.
// Sans cette correspondance, l'encart « Modèle » afficherait la valeur brute au lieu
// du libellé.
const SERVICES_OPTIONS_KEYS: Partial<Record<string, keyof ServicesOptions>> = {
  kind: "kinds",
  feeCondition: "feeConditions",
  updateFrequency: "updateFrequencies",
};

function getFieldOptions(fieldName: string, servicesOptions: ServicesOptions) {
  const optionsKey = SERVICES_OPTIONS_KEYS[fieldName] ?? fieldName;
  return optionsKey in servicesOptions ? servicesOptions[optionsKey] : null;
}

export function getModelInputProps({
  service,
  servicesOptions,
  showModel,
  onUseModelValue,
  model,
  schema,
}: {
  service: Service;
  servicesOptions: ServicesOptions;
  showModel: boolean;
  onUseModelValue: (fieldName: string) => void;
  model?: Model;
  schema?: Schema;
}) {
  return schema
    ? Object.fromEntries(
        Object.keys(schema).map((fieldName) => [
          fieldName,
          {
            showModel,
            value: model ? model[fieldName] : undefined,
            serviceValue: service[fieldName],
            options: getFieldOptions(fieldName, servicesOptions),
            onUseValue: () => onUseModelValue(fieldName),
          },
        ])
      )
    : {};
}
