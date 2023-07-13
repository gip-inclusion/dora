export type AdminDivisionType =
  | "country"
  | "region"
  | "department"
  | "epci"
  | "city";

export type ServiceCategory =
  | "acces-aux-droits-et-citoyennete"
  | "accompagnement-social-et-professionnel-personnalise"
  | "apprendre-francais"
  | "creation-activite"
  | "gestion-financiere"
  | "choisir-un-metier"
  | "preparer-sa-candidature"
  | "trouver-un-emploi"
  | "equipement-et-alimentation"
  | "famille"
  | "handicap"
  | "illettrisme"
  | "logement-hebergement"
  | "mobilite"
  | "numerique"
  | "remobilisation"
  | "sante";

export type ModerationStatus =
  | "NEED_INITIAL_MODERATION"
  | "NEED_NEW_MODERATION"
  | "IN_PROGRESS"
  | "VALIDATED";

export type GeoApiValue = {
  code: string;
  name: string;
  similarity: number;
  geom?: object;
};

export type LocationKind = "a-distance" | "en-presentiel";

export type ServiceStatus = "DRAFT" | "SUGGESTION" | "PUBLISHED" | "ARCHIVED";

export interface StructureService {
  address1: string;
  address2: string;
  categoriesDisplay: string[];
  category: string;
  categoryDisplay: string;
  city_code: string;
  city: string;
  contactEmail: string;
  contactName: string;
  contactPhone: string;
  department: string;
  diffusionZoneDetailsDisplay: string;
  diffusionZoneType: AdminDivisionType;
  diffusionZoneTypeDisplay: string;
  isAvailable: boolean;
  isCumulative: boolean;
  locationKinds: LocationKind;
  locationKindsDisplay: string;
  model: string;
  modelChanged: boolean;
  modelName: boolean;
  modificationDate: string;
  name: string;
  postalCode: string;
  remoteUrl: string;
  shortDesc: string;
  slug: string;
  status: ServiceStatus;
  structure: string;
  useInclusionNumeriqueScheme: boolean;
}

export interface StructureModel {
  slug: string;
  name: string;
  department: string;
  modificationDate: string;
  categoriesDisplay: string[];
  shortDesc: string;
  structure: string;
  numServices: boolean;
}

export interface Branches {
  department: string;
  modificationDate: string;
  name: string;
  numServices: number | undefined;
  slug: string;
  typologyDisplay: string;
}

export interface ShortStructure {
  department: string;
  modificationDate: string;
  name: string;
  parent: string;
  siret: string;
  slug: string;
  typologyDisplay: string;
}

export interface AdminShortStructure {
  department: string;
  modificationDate: string;
  name: string;
  parent: string;
  siret: string;
  slug: string;
  latitude: number;
  longitude: number;
  typology: string;
  typologyDisplay: string;
  categories: ServiceCategory[];
  hasAdmin: boolean;
  moderationDate: string;
  moderationStatus: ModerationStatus;
  numPublishedServices: number;
  numOutdatedServices: number;
  numServices: number;
  shortDesc: string;
}

export interface StructureSource {
  value: string;
  label: string;
}
export interface Structure {
  accesslibreUrl: string;
  address1: string;
  address2: string;
  ape: string;
  archivedServices: StructureService[];
  branches: Branches[];
  canEditInformations: boolean;
  canEditMembers: boolean;
  canEditServices: boolean;
  canInviteFirstAdmin: boolean;
  canViewMembers: boolean;
  city: string;
  cityCode: string;
  codeSafirPe: string;
  creationDate: string;
  department: string;
  email: string;
  fullDesc: string;
  hasAdmin: boolean;
  hasBeenEdited: boolean;
  isAdmin: boolean;
  isMember: boolean;
  isPendingMember: boolean;
  latitude: number;
  longitude: number;
  models: StructureModel[];
  modificationDate: string;
  name: string;
  nationalLabels: string[];
  numModels: number;
  numServices: number;
  openingHours: string | null;
  openingHoursDetails: string | null;
  otherLabels: string;
  parent: string;
  phone: number;
  postalCode: string;
  quickStartDone: boolean;
  services: StructureService[];
  shortDesc: string;
  siret: string | null;
  slug: string;
  source: StructureSource;
  typologyDisplay: string;
  typology: number;
  url: string;
}

interface StructureMemberUserInfos {
  email: string;
  firstName: string;
  fullName: string;
  lastName: string;
}
export interface StructureMember {
  id: string;
  isAdmin: boolean;
  user: StructureMemberUserInfos;
}
export interface PutativeStructureMember {
  id: string;
  invitedByAdmin: boolean;
  isAdmin: boolean;
  user: StructureMemberUserInfos;
}

export interface Establishment {
  address1: string;
  address2: string;
  ape: string;
  city: string;
  cityCode: string;
  isSiege: boolean;
  latitude: number;
  longitude: number;
  name: "string";
  postalCode: "string";
  siren: "string";
  siret: "string";
}

export interface NationalLabel {
  value: string;
  label: string;
}

export interface Typology {
  value: string;
  label: string;
}

export interface StructuresOptions {
  nationalLabels: NationalLabel[];
  sources: StructureSource[];
  typologies: Typology[];
}

// OSM hours format
export type OsmPeriodDay = {
  isOpen: boolean;
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

export type ServiceUpdateStatus = "NOT_NEEDED" | "NEEDED" | "REQUIRED" | "ALL";

export type ServiceKind =
  | "accompagnement"
  | "accueil"
  | "aide-financiere"
  | "aide-materielle"
  | "atelier"
  | "autonomie"
  | "delegation"
  | "financement"
  | "formation"
  | "information"
  | "numerique";

export type FeeCondition =
  | "gratuit"
  | "gratuit-sous-conditions"
  | "payant"
  | "adhesion"
  | "pass-numerique";

export type CoachOrientationModes =
  | "envoyer-courriel"
  | "envoyer-fiche-prescription"
  | "envoyer-formulaire"
  | "autre"
  | "telephoner";
export type BeneficiaryAccessModes =
  | "envoyer-courriel"
  | "se-presenter"
  | "autre"
  | "telephoner";

export interface SearchQuery {
  categoryIds: string[];
  subCategoryIds: string[];
  cityCode: string;
  cityLabel: string;
  kindIds: ServiceKind[];
  feeConditions: FeeCondition[];
}

export interface ServiceSearchResult {
  distance: number;
  location: string;
  diffusionZoneType: string;
  modificationDate: string;
  name: string;
  shortDesc: string;
  slug: string;
  structure: string;
  status: ServiceStatus;
  updateStatus: ServiceUpdateStatus;
  structureInfo: {
    address1: string;
    address2: string;
    city: string;
    name: string;
    postalCode: string;
    shortDesc: string;
    siret: string;
    slug: string;
    url: string;
  };
}

export interface FileInfo {
  url: string;
  name: string;
}

export type CustomizableFK = number | string;

export interface ServiceStructure {
  address1: string;
  address2: string;
  city: string;
  department: string;
  hasAdmin: boolean;
  name: string;
  numServices: number;
  postalCode: string;
  shortDesc: string;
  siret: string;
  slug: string;
  url: string;
}

export interface Point {
  type: "Point";
  coordinates: [longitude: number, latitude: number];
}

export interface Service {
  markSynced?: boolean;
  accessConditions: CustomizableFK[];
  accessConditionsDisplay: string[];
  address1: string;
  address2: string;
  beneficiariesAccessModes: BeneficiaryAccessModes[];
  beneficiariesAccessModesDisplay: string[];
  beneficiariesAccessModesOther: string;
  canWrite: boolean;
  categories: ServiceCategory[];
  categoriesDisplay: string[];
  category: ServiceCategory;
  categoryDisplay: string;
  city: string;
  cityCode: string;
  coachOrientationModes: CoachOrientationModes[];
  coachOrientationModesDisplay: string[];
  coachOrientationModesOther: string;
  concernedPublic: CustomizableFK[]; // TODO: should be plural
  concernedPublicDisplay: string[];
  contactEmail: string;
  contactName: string;
  contactPhone: string;
  creationDate: string;
  credentials: CustomizableFK[];
  credentialsDisplay: string[];
  department: string;
  diffusionZoneDetails: string;
  diffusionZoneDetailsDisplay: string;
  diffusionZoneType: AdminDivisionType;
  diffusionZoneTypeDisplay: string;
  feeCondition: FeeCondition;
  feeDetails: string;
  fillingDuration: number;
  forms: string[];
  formsInfo: FileInfo[];
  fullDesc: string;
  geom: Point;
  hasAlreadyBeenUnpublished: boolean;
  isAvailable: boolean;
  isContactInfoPublic: boolean;
  isCumulative: boolean;
  kinds: ServiceKind[];
  kindsDisplay: string[];
  locationKinds: LocationKind[];
  locationKindsDisplay: string[];
  model: string;
  modelChanged: boolean;
  modificationDate: string;
  name: string;
  onlineForm: string;
  postalCode: string;
  publicationDate: string;
  qpvOrZrr: boolean;
  recurrence: string;
  remoteUrl: string;
  requirements: CustomizableFK[];
  requirementsDisplay: string[];
  shortDesc: string;
  slug: string;
  status: ServiceStatus;
  structure: string;
  structureInfo: ServiceStructure;
  subcategories: string[];
  subcategoriesDisplay: string[];
  suspensionDate: string;
  useInclusionNumeriqueScheme: boolean;
  updateStatus: ServiceUpdateStatus;
}

export interface ShortService {
  categoriesDisplay: string[];
  category: string;
  categoryDisplay: string[];
  coachOrientationModes: CoachOrientationModes[];
  contactEmail: string;
  contactName: string;
  contactPhone: string;
  city: string;
  department: string;
  diffusionZoneDetailsDisplay: string;
  diffusionZoneType: AdminDivisionType;
  diffusionZoneTypeDisplay: string;
  model: string;
  modelChanged: boolean;
  modificationDate: string;
  name: string;
  postalCode: string;
  shortDesc: string;
  slug: string;
  status: ServiceStatus;
  structure: string;
  structureInfo: ServiceStructure;
  locationKinds: LocationKind;
  useInclusionNumeriqueScheme: boolean;
  updateStatus: ServiceUpdateStatus;
}

export interface Bookmark {
  service: ShortService;
  creationDate: string;
}

export interface CustomChoice {
  value: number;
  label: string;
  structure: string | null;
}

export type ServicesOptions = {
  accessConditions: CustomChoice[];
  beneficiariesAccessModes: { value: BeneficiaryAccessModes; label: string }[];
  categories: { value: ServiceCategory; label: string }[];
  coachOrientationModes: { value: CoachOrientationModes; label: string }[];

  concernedPublic: CustomChoice[];
  credentials: CustomChoice[];
  deploymentDepartments: string[];
  diffusionZoneType: { value: AdminDivisionType; label: string }; // TODO: should be plural
  feeConditions: { value: FeeCondition; label: string }[];
  kinds: { value: ServiceKind; label: string }[];
  locationKinds: { value: LocationKind; label: string }[];
  requirements: CustomChoice[];
  subcategories: { value: string; label: string }[];
};

export type Model = {
  accessConditions: CustomizableFK[];
  accessConditionsDisplay: string[];
  beneficiariesAccessModes: BeneficiaryAccessModes[];
  beneficiariesAccessModesDisplay: string[];
  beneficiariesAccessModesOther: string;
  canWrite: boolean;
  categories: ServiceCategory[];
  categoriesDisplay: string[];
  coachOrientationModes: CoachOrientationModes[];
  coachOrientationModesDisplay: string[];
  coachOrientationModesOther: string;
  concernedPublic: CustomizableFK[];
  concernedPublicDisplay: string[];
  creationDate: string;
  credentials: CustomizableFK[];
  credentialsDisplay: string[];
  department: string;
  feeCondition: FeeCondition;
  feeDetails: string;
  forms: string[];
  formsInfo: FileInfo[];
  fullDesc: string;
  isCumulative: boolean;
  kinds: ServiceKind[];
  kindsDisplay: string[];
  modificationDate: string;
  name: string;
  numServices: number;
  onlineForm: string;
  qpvOrZrr: string;
  recurrence: string;
  requirements: CustomizableFK[];
  requirementsDisplay: string[];
  shortDesc: string;
  slug: string;
  structure: string;
  structureInfo: ServiceStructure;
  subcategories: string[];
  subcategoriesDisplay: string[];
  suspensionDate: string;
};

export type Partner = {
  name: string;
  img: string;
};

// FORM
export type Choice<T = string> = {
  value: T;
  label: string;
  optGroupKey?: string;
  selectedLabel?: string;
  icon?: string;
  iconOnRight?: boolean;
};

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

type ContactPreferences = "TELEPHONE" | "EMAIL" | "AUTRE";

export interface Orientation {
  // Tous les champs de l'étape 1 pouvant être optionnels
  // on est contraint de se baser sur un booléen pour s'assurer que l'étape 1 a bien été visionnée
  firstStepDone: boolean;

  situation: string[];
  situationOther: string;
  requirements: string[];

  referentLastName: string;
  referentFirstName: string;
  referentPhone: string;
  referentEmail: string;
  prescriberStructureSlug: string;

  beneficiaryLastName: string;
  beneficiaryFirstName: string;
  beneficiaryAvailability: string | null;
  beneficiaryContactPreferences: ContactPreferences[];
  beneficiaryPhone: string;
  beneficiaryEmail: string;
  beneficiaryOtherContactMethod: string;
  orientationReasons: string;

  attachments: { [key: string]: string[] };

  // Champs après la création de l'orientation
  id?: number;
  queryId?: string;
  creationDate?: string;
  prescriberStructure?: {
    name: string;
    slug: string;
  };
  processingDate?: string;
  status?: "OUVERTE" | "VALIDÉE" | "REFUSÉE";
  beneficiaryAttachments?: string[];
  service?: {
    name: string;
    slug: string;
  };
  prescriber?: {
    name: string;
    email: string;
  };
}
