import type { FeeCondition, LocationKind, ServicesOptions } from "$lib/types";
import * as v from "../schema-utils";

export function allCategoriesHaveSubcategories() {
  return (name, value, data, servicesOptions: ServicesOptions) => {
    const subcatRoots = new Set(
      data.subcategories.map((val) => val.split("--")[0])
    );

    if (!servicesOptions) {
      return {
        valid: true,
      };
    }
    const catWithoutSubCat = data.categories
      .filter((val) => !subcatRoots.has(val))
      .map(
        (val) =>
          servicesOptions.categories.find((cat) => cat.value === val).label
      );
    return {
      valid: catWithoutSubCat.length === 0,
      msg: `Ces thématiques n’ont pas de besoin associé: ${catWithoutSubCat.join(
        ", "
      )} `,
    };
  };
}

export const serviceSchema: v.Schema = {
  structure: {
    label: "Structure",
    default: "",
    rules: [v.isString(), v.maxStrLength(50)],
    required: true,
  },
  name: {
    label: "Titre",
    default: "",
    rules: [
      v.isString(),
      v.minStrLength(3),
      v.maxStrLength(150),
      v.doesNotEndWithAPeriod(),
      v.isNotAllUpperCase(),
    ],
    post: [v.trim],
    required: true,
    maxLength: 150,
  },
  description: {
    label: "Description",
    default: "",
    rules: [v.isString()],
    post: [v.trim],
    required: true,
  },
  categories: {
    label: "Thématiques",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    required: true,
  },
  subcategories: {
    label: "Besoins",
    default: [],
    rules: [
      v.isArray([v.isString(), v.maxStrLength(255)]),
      allCategoriesHaveSubcategories(),
    ],
    required: true,
  },
  kind: {
    label: "Type",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    required: true,
  },
  fundingLabels: {
    label: "Financeur(s)",
    default: [],
    rules: [v.isArray([])],
  },
  publics: {
    label: "Choix du public",
    default: [],
    rules: [v.isArray([v.isString()])],
  },
  publicsPrecisions: {
    label: "Précisions concernant les publics",
    default: "",
    rules: [v.isString()],
  },
  conditionsAcces: {
    label: "Conditions d'accès",
    default: "",
    rules: [v.isString()],
  },
  forms: {
    label: "Documents à fournir",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
    required: false,
  },
  feeCondition: {
    label: "Frais à charge",
    default: "gratuit",
    rules: [v.isString()],
  },
  feeDetails: {
    label: "Détails des frais à charge",
    default: "",
    post: [v.trim],
    rules: [v.isString()],
    required: (data: { feeCondition: FeeCondition }) => {
      return data.feeCondition !== "gratuit";
    },
  },
  mobilisableBy: {
    label: "Mobilisable par…",
    default: [],
    rules: [v.isArray([v.isString()])],
  },
  mobilisationModes: {
    label: "Mode de mobilisation du service",
    default: [],
    rules: [v.isArray([v.isString()])],
    required: true,
  },
  mobilisationLink: {
    label: "Configuration du formulaire",
    default: null,
    rules: [v.isURL()],
  },
  mobilisationDetails: {
    label: "Précisions sur les modalités",
    default: "",
    rules: [v.isString()],
    post: [v.trim],
  },
  zoneEligibilite: {
    label: "Secteurs éligibles",
    default: [],
    rules: [v.isArray([])],
  },
  locationKinds: {
    label: "Mode d’accueil",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    required: true,
  },
  address1: {
    label: "Adresse",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    maxLength: 255,
    required: false,
  },
  address2: {
    label: "Complément d’adresse",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    maxLength: 255,
    required: false,
  },
  postalCode: {
    label: "Code postal",
    default: "",
    rules: [v.isPostalCode()],
    maxLength: 5,
    required: (data: { locationKinds: LocationKind[] }) => {
      return data.locationKinds.includes("en-presentiel");
    },
  },
  city: {
    label: "Ville",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    maxLength: 255,
    required: (data: { locationKinds: LocationKind[] }) => {
      return data.locationKinds.includes("en-presentiel");
    },
  },
  durationWeeklyHours: {
    label: "Nombre d'heures par semaine",
    default: null,
    post: [v.toNumber],
    rules: [v.isPositiveInteger(), v.minNum(1)],
    minNumber: 1,
  },
  durationWeeks: {
    label: "Nombre de semaines",
    default: null,
    post: [v.toNumber],
    rules: [v.isPositiveInteger(), v.minNum(1)],
    minNumber: 1,
  },
  openingHours: {
    label: "Horaires du service",
    default: "",
    rules: [v.isString()],
  },
  contactName: {
    label: "Prénom et nom",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    maxLength: 140,
  },
  contactPhone: {
    label: "Téléphone",
    default: "",
    pre: [v.removeAllNonDigits],
    rules: [v.isPhone()],
    maxLength: 10,
    required: true,
  },
  contactEmail: {
    label: "Courriel",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    required: true,
  },
  isContactInfoPublic: {
    label: "Rendre les informations de contact publiques",
    default: false,
    rules: [v.isBool()],
    required: true,
  },
  updateFrequency: {
    label: "Périodicité de mise à jour",
    default: "tous-les-6-mois",
    rules: [v.isString()],
    required: true,
  },
};

export const modelSchema: v.Schema = {
  structure: serviceSchema.structure,
  name: serviceSchema.name,
  description: serviceSchema.description,
  categories: serviceSchema.categories,
  subcategories: serviceSchema.subcategories,
  kind: serviceSchema.kind,
  fundingLabels: serviceSchema.fundingLabels,
  publics: serviceSchema.publics,
  publicsPrecisions: serviceSchema.publicsPrecisions,
  conditionsAcces: serviceSchema.conditionsAcces,
  forms: serviceSchema.forms,
  feeCondition: serviceSchema.feeCondition,
  feeDetails: serviceSchema.feeDetails,
  mobilisableBy: serviceSchema.mobilisableBy,
  mobilisationLink: serviceSchema.mobilisationLink,
  mobilisationModes: serviceSchema.mobilisationModes,
  mobilisationDetails: serviceSchema.mobilisationDetails,
  durationWeeklyHours: serviceSchema.durationWeeklyHours,
  durationWeeks: serviceSchema.durationWeeks,
  updateFrequency: serviceSchema.updateFrequency,
};
