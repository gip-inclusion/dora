import type {
  Model,
  Service,
  ServiceStructure,
  ServicesOptions,
  Structure,
} from "$lib/types";
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

// `structureInfo` est calculé par le back et n'appartient donc pas au schéma : un service
// en cours de création ne l'a pas tant qu'on n'a pas chargé la structure choisie. Les boutons
// « utiliser les infos de la structure » le lisent, d'où cette projection.
export function toServiceStructure(structure: Structure): ServiceStructure {
  return {
    address1: structure.address1,
    address2: structure.address2,
    city: structure.city,
    department: structure.department,
    email: structure.email,
    hasAdmin: structure.hasAdmin,
    name: structure.name,
    numServices: structure.numServices,
    openingHours: structure.openingHours,
    phone: structure.phone,
    postalCode: structure.postalCode,
    shortDesc: structure.shortDesc,
    siret: structure.siret ?? "",
    slug: structure.slug,
    url: structure.url,
  };
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
