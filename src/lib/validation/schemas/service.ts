import type {
  BeneficiaryAccessModes,
  CoachOrientationModes,
  AdminDivisionType,
  FeeCondition,
  LocationKind,
  ServicesOptions,
} from "$lib/types";
import * as v from "../schema-utils";

export function allCategoriesHaveSubcategories() {
  return (name, value, data, servicesOptions: ServicesOptions) => {
    const subcatRoots = new Set(
      data.subcategories.map((val) => val.split("--")[0])
    );

    if (!servicesOptions) {
      console.log("Missing servicesOptions in rules check");
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
  siret: {
    label: "SIRET",
    default: "",
    rules: [v.isSiret()],
    maxLength: 14,
  },
  structure: {
    label: "Structure",
    default: "",
    rules: [v.isString(), v.maxStrLength(50)],
    required: true,
  },
  categories: {
    label: "Thématiques",
    default: [],
    rules: [
      v.isArray([v.isString(), v.maxStrLength(255)]),
      v.arrMaxLength(3, "Vous avez choisi plus de 3 thématiques"),
    ],
    dependents: ["subcategories"],
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
  kinds: {
    label: "Types",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    required: true,
  },
  name: {
    label: "Titre",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    required: true,
    maxLength: 140,
  },
  shortDesc: {
    label: "Résumé",
    default: "",
    rules: [v.isString(), v.maxStrLength(280)],
    post: [v.trim],
    maxLength: 280,
    required: true,
  },
  recurrence: {
    label: "Fréquence et horaires",
    default: "",
    rules: [v.isString(), v.maxStrLength(140)],
    post: [v.trim],
    maxLength: 140,
  },
  fullDesc: {
    label: "Description",
    default: "",
    rules: [v.isString()],
    post: [v.trim],
  },
  accessConditions: {
    label: "Critères",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  concernedPublic: {
    label: "Profils",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  requirements: {
    label: "Pré-requis ou compétences",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  isCumulative: {
    label: "Cumulable",
    default: true,
    rules: [v.isBool()],
  },
  feeCondition: {
    label: "Frais à charge",
    default: "gratuit",
    rules: [v.isString()],
    dependents: ["feeDetails"],
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
  beneficiariesAccessModes: {
    label: "Pour les bénéficiaires",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    dependents: [
      "contactEmail",
      "contactPhone",
      "beneficiariesAccessModesOther",
      "coachOrientationModes",
    ],
    required: (data: { coachOrientationModes: CoachOrientationModes }) => {
      return !data.coachOrientationModes.length;
    },
  },
  beneficiariesAccessModesOther: {
    label: "",
    default: "",
    rules: [v.isString(), v.maxStrLength(280)],
    maxLength: 280,
    required: (data: { beneficiariesAccessModes: BeneficiaryAccessModes }) => {
      return data.beneficiariesAccessModes.includes("autre");
    },
  },
  coachOrientationModes: {
    label: "Pour les accompagnateurs",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    dependents: [
      "contactEmail",
      "contactPhone",
      "coachOrientationModesOther",
      "beneficiariesAccessModes",
    ],
    required: (data: { beneficiariesAccessModes: BeneficiaryAccessModes }) => {
      return !data.beneficiariesAccessModes.length;
    },
  },
  coachOrientationModesOther: {
    label: "",
    default: "",
    rules: [v.isString(), v.maxStrLength(280)],
    required: (data: { coachOrientationModes: CoachOrientationModes }) => {
      return data.coachOrientationModes.includes("autre");
    },
    maxLength: 280,
  },

  credentials: {
    label: "Justificatifs à fournir",
    default: [],
    rules: [v.isArray([v.isCustomizablePK()])],
  },
  forms: {
    label: "Documents à compléter",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(1024)])],
  },
  onlineForm: {
    label: "Lien",
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
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
    required: (data: {
      coachOrientationModes: CoachOrientationModes;
      beneficiariesAccessModes: BeneficiaryAccessModes;
    }) => {
      return (
        data.coachOrientationModes.includes("telephoner") ||
        data.beneficiariesAccessModes.includes("telephoner")
      );
    },
  },
  contactEmail: {
    label: "Courriel",
    default: "",
    rules: [v.isEmail(), v.maxStrLength(254)],
    post: [v.lower, v.trim],
    maxLength: 254,
    required: (data: {
      coachOrientationModes: CoachOrientationModes;
      beneficiariesAccessModes: BeneficiaryAccessModes;
    }) => {
      return (
        data.coachOrientationModes.includes("envoyer-courriel") ||
        data.coachOrientationModes.includes("envoyer-fiche-prescription") ||
        data.beneficiariesAccessModes.includes("envoyer-courriel")
      );
    },
  },
  isContactInfoPublic: {
    label: "Rendre les informations de contact publiques",
    default: false,
    rules: [v.isBool()],
    required: true,
  },
  locationKinds: {
    label: "Mode d’accueil",
    default: [],
    rules: [v.isArray([v.isString(), v.maxStrLength(255)])],
    dependents: ["city", "address1", "postalCode"],
    required: true,
  },
  remoteUrl: {
    label: "Lien visioconférence",
    default: "",
    rules: [v.isURL(), v.maxStrLength(200)],
    post: [v.trim],
    maxLength: 200,
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
  address1: {
    label: "Adresse",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    dependents: ["postalCode"],
    maxLength: 255,
    required: (data: { locationKinds: LocationKind[] }) => {
      return data.locationKinds.includes("en-presentiel");
    },
  },
  address2: {
    label: "Complément d’adresse",
    default: "",
    rules: [v.isString(), v.maxStrLength(255)],
    post: [v.trim],
    maxLength: 255,
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
  diffusionZoneType: {
    label: "Périmètre",
    default: "",
    rules: [v.isString(), v.maxStrLength(10)],
    dependents: ["diffusionZoneDetails"],
    required: true,
  },

  diffusionZoneDetails: {
    label: "Territoire",
    default: "",
    rules: [v.isString(), v.maxStrLength(9)],
    maxLength: 9,
    required: (data: { diffusionZoneType: AdminDivisionType }) => {
      return data.diffusionZoneType !== "country";
    },
  },
  qpvOrZrr: {
    label: "Uniquement QPV ou ZRR",
    default: false,
    rules: [v.isBool()],
  },
  suspensionDate: {
    label: "Date de fin",
    default: null,
    rules: [v.isDate()],
    post: [v.nullEmpty],
  },
  useInclusionNumeriqueScheme: {
    label: "",
    default: false,
    rules: [v.isBool()],
  },
};

export const inclusionNumeriqueSchema: v.Schema = {
  structure: serviceSchema.structure,
  categories: serviceSchema.categories,
  subcategories: serviceSchema.subcategories,
  kinds: serviceSchema.kinds,
  concernedPublic: serviceSchema.concernedPublic,
  feeCondition: serviceSchema.feeCondition,
  feeDetails: serviceSchema.feeDetails,
  beneficiariesAccessModes: {
    ...serviceSchema.beneficiariesAccessModes,
    required: true,
  },
  beneficiariesAccessModesOther: serviceSchema.beneficiariesAccessModesOther,
  contactName: serviceSchema.contactName,
  contactPhone: serviceSchema.contactPhone,
  contactEmail: serviceSchema.contactEmail,
  isContactInfoPublic: serviceSchema.isContactInfoPublic,
  city: serviceSchema.city,
  address1: serviceSchema.address1,
  address2: serviceSchema.address2,
  postalCode: serviceSchema.postalCode,
  diffusionZoneType: serviceSchema.diffusionZoneType,
  diffusionZoneDetails: serviceSchema.diffusionZoneDetails,
  useInclusionNumeriqueScheme: serviceSchema.useInclusionNumeriqueScheme,
};

export const draftSchema: v.Schema = {
  structure: serviceSchema.structure,
  categories: serviceSchema.categories,
  subcategories: serviceSchema.subcategories,
  kinds: serviceSchema.kinds,
  name: serviceSchema.name,
  shortDesc: serviceSchema.shortDesc,
  fullDesc: serviceSchema.fullDesc,
  accessConditions: serviceSchema.accessConditions,
  concernedPublic: serviceSchema.concernedPublic,
  requirements: serviceSchema.requirements,
  isCumulative: serviceSchema.isCumulative,
  feeCondition: serviceSchema.feeCondition,
  feeDetails: serviceSchema.feeDetails,
  beneficiariesAccessModes: serviceSchema.beneficiariesAccessModes,
  beneficiariesAccessModesOther: serviceSchema.beneficiariesAccessModesOther,
  coachOrientationModes: serviceSchema.coachOrientationModes,
  coachOrientationModesOther: serviceSchema.coachOrientationModesOther,
  credentials: serviceSchema.credentials,
  forms: serviceSchema.forms,
  onlineForm: serviceSchema.onlineForm,
  contactName: serviceSchema.contactName,
  contactPhone: serviceSchema.contactPhone,
  contactEmail: serviceSchema.contactEmail,
  isContactInfoPublic: serviceSchema.isContactInfoPublic,
  locationKinds: serviceSchema.locationKinds,
  remoteUrl: serviceSchema.remoteUrl,
  city: serviceSchema.city,
  address1: serviceSchema.address1,
  address2: serviceSchema.address2,
  postalCode: serviceSchema.postalCode,
  diffusionZoneType: serviceSchema.diffusionZoneType,
  diffusionZoneDetails: serviceSchema.diffusionZoneDetails,
  qpvOrZrr: serviceSchema.qpvOrZrr,
  recurrence: serviceSchema.recurrence,
  suspensionDate: serviceSchema.suspensionDate,
  useInclusionNumeriqueScheme: serviceSchema.useInclusionNumeriqueScheme,
};

export const contribSchema: v.Schema = {
  siret: serviceSchema.siret,
  categories: serviceSchema.categories,
  subcategories: serviceSchema.subcategories,
  kinds: serviceSchema.kinds,
  name: serviceSchema.name,
  shortDesc: serviceSchema.shortDesc,
  fullDesc: serviceSchema.fullDesc,
  accessConditions: serviceSchema.accessConditions,
  concernedPublic: serviceSchema.concernedPublic,
  requirements: serviceSchema.requirements,
  isCumulative: serviceSchema.isCumulative,
  feeCondition: serviceSchema.feeCondition,
  feeDetails: serviceSchema.feeDetails,
  contactName: serviceSchema.contactName,
  contactPhone: { ...serviceSchema.contactPhone, required: false },
  contactEmail: { ...serviceSchema.contactEmail, required: false },
  locationKinds: { ...serviceSchema.locationKinds, required: false },
  remoteUrl: serviceSchema.remoteUrl,
  city: serviceSchema.city,
  address1: serviceSchema.address1,
  address2: serviceSchema.address2,
  postalCode: serviceSchema.postalCode,
};

export const modelSchema: v.Schema = {
  structure: serviceSchema.structure,
  categories: serviceSchema.categories,
  subcategories: serviceSchema.subcategories,
  kinds: serviceSchema.kinds,
  name: serviceSchema.name,
  shortDesc: serviceSchema.shortDesc,
  fullDesc: serviceSchema.fullDesc,
  accessConditions: serviceSchema.accessConditions,
  concernedPublic: serviceSchema.concernedPublic,
  requirements: serviceSchema.requirements,
  isCumulative: serviceSchema.isCumulative,
  feeCondition: serviceSchema.feeCondition,
  feeDetails: serviceSchema.feeDetails,
  beneficiariesAccessModes: serviceSchema.beneficiariesAccessModes,
  beneficiariesAccessModesOther: serviceSchema.beneficiariesAccessModesOther,
  coachOrientationModes: serviceSchema.coachOrientationModes,
  coachOrientationModesOther: serviceSchema.coachOrientationModesOther,
  credentials: serviceSchema.credentials,
  forms: serviceSchema.forms,
  onlineForm: serviceSchema.onlineForm,
  recurrence: serviceSchema.recurrence,
  suspensionDate: serviceSchema.suspensionDate,
};
