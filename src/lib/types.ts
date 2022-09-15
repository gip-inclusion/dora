// STRUCTURE
export type Structure = {
  name: string;
  slug: string;
  siret: string;
  url: string | undefined;
  email: string | undefined;
  phone: string | undefined;
  openingHours: string | undefined;
  openingHoursDetails: string | undefined;
  shortDesc: string;
  fullDesc: string;
  isAdmin: boolean;
  address1: string;
  address2: string;
  latitude: number;
  longitude: number;
  postalCode: number;
  cityCode: number;
  city: string;

  nationalLabels: string[];
  otherLabels: string;
  ape: string;

  typologyDisplay: string;
  numServices: number;
  accesslibreUrl: string | undefined;
  modificationDate: string;
};

export type StructuresOptions = {
  nationalLabels: { value: string; label: string }[];
  typologies: { value: string; label: string }[];
};

// OSM hours format
export type OsmPeriodDay = {
  isOpen: boolean;
  touched: boolean;
  openAt: string;
  closeAt: string;
};
export type OsmDay = {
  timeSlot1: OsmPeriodDay;
  timeSlot2: OsmPeriodDay;
};

export type OsmOpeningHours = {
  monday: OsmDay;
  tuesday: OsmDay;
  wednesday: OsmDay;
  thursday: OsmDay;
  friday: OsmDay;
  saturday: OsmDay;
  sunday: OsmDay;
};

// SERVICES
export enum SERVICE_STATUSES {
  DRAFT = "DRAFT",
  SUGGESTION = "SUGGESTION",
  PUBLISHED = "PUBLISHED",
  ARCHIVED = "ARCHIVED",
}

export enum SERVICE_UPDATE_STATUS {
  NOT_NEEDED = "NOT_NEEDED",
  NEEDED = "NEEDED",
  REQUIRED = "REQUIRED",
}

export type Service = {
  name: string;
  slug: string;
  contactName: string | undefined;
  contactPhone: string | undefined;
  contactEmail: string | undefined;

  subcategories: string[] | undefined;

  beneficiariesAccessModesDisplay: string[] | undefined;
  beneficiariesAccessModesOther: string | undefined;

  coachOrientationModesDisplay: string[] | undefined;
  coachOrientationModesOther: string | undefined;

  accessConditions: string[] | undefined;
  accessConditionsDisplay: string[] | undefined;

  credentialsDisplay: string[] | undefined;

  concernedPublicDisplay: string[] | undefined;
  requirementsDisplay: string[] | undefined;

  locationKinds: string[] | undefined;
  remoteUrl: string | undefined;
  postalCode: string | undefined;
  address1: string | undefined;
  address2: string | undefined;
  city: string | undefined;
  department: string;
  isContactInfoPublic: boolean;

  isAvailable: boolean;
  qpvOrZrr: boolean;
  structureInfo: Structure;
  canWrite: boolean;
  structure: string;
  status: SERVICE_STATUSES;
  model: string | undefined;
  modelChanged: boolean | undefined;
  hasAlreadyBeenUnpublished: boolean;
  isCumulative: boolean;
  hasFee: boolean;
  feeDetails: string | undefined;
  recurrence: string | undefined;
  creationDate: string;
  modificationDate: string | undefined;
  diffusionZoneDetailsDisplay: string | undefined;

  onlineForm: string | undefined;

  formsInfo: { url: string; name: string }[] | undefined;

  kindsDisplay: string[] | undefined;

  shortDesc: string | undefined;
  fullDesc: string | undefined;
};

export type DashboardService = Pick<
  Service,
  | "name"
  | "slug"
  | "contactName"
  | "contactPhone"
  | "contactEmail"
  | "postalCode"
  | "city"
  | "department"
  | "status"
  | "modificationDate"
  | "shortDesc"
  | "diffusionZoneDetailsDisplay"
  | "modelChanged"
  | "isAvailable"
  | "isCumulative"
  | "feeDetails"
  | "recurrence"
  | "locationKinds"
  | "address1"
  | "address2"
  | "remoteUrl"
  | "hasFee"
  | "model"
  | "structure"
  | "qpvOrZrr"
>;

export type ServicesOptions = {
  categories: { value: string; label: string }[];
  subcategories: { value: string; label: string }[];
};

// FORM
export type Day =
  | "monday"
  | "tuesday"
  | "wednesday"
  | "thursday"
  | "friday"
  | "saturday"
  | "sunday";
export type DayPrefix = "Mo" | "Tu" | "We" | "Th" | "Fr" | "Sa" | "Su";
export type DayPeriod = "timeSlot1" | "timeSlot2";
