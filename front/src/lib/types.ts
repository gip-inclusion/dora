import type { Component } from "svelte";

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
  similarity?: number;
  geom?: object;
};

export type LocationKind = "a-distance" | "en-presentiel";

export type ServiceStatus = "DRAFT" | "SUGGESTION" | "PUBLISHED" | "ARCHIVED";

export interface StructureService {
  address1: string;
  address2: string;
  categoriesDisplay: string[];
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
  locationKinds: LocationKind[];
  locationKindsDisplay: string[];
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
  updateNeeded: boolean;
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
  numServices?: number;
  slug: string;
  typologyDisplay: string;
}

export interface ShortStructure {
  department: string;
  modificationDate: string;
  name: string;
  noDoraForm: boolean;
  parent: string;
  siret: string;
  slug: string;
  typologyDisplay: string;
  canEditInformations: boolean;
  servicesToUpdate: { name: string; slug: string }[];
}

export interface AdminShortStructure {
  categories: ServiceCategory[];
  city: string;
  department: string;
  email: string;
  hasAdmin: boolean;
  isObsolete: boolean;
  latitude: number;
  longitude: number;
  moderationDate: string;
  moderationStatus: ModerationStatus;
  modificationDate: string;
  name: string;
  nationalLabels: string[];
  numDraftServices: number;
  numOutdatedServices: number;
  numPublishedServices: number;
  numServices: number;
  parent: string;
  phone: string;
  shortDesc: string;
  siret: string;
  slug: string;
  typology: string;
  typologyDisplay: string;
  admins: string[];
  editors: string[];
  adminsToModerate: string[];
  adminsToRemind: string[];
  numPotentialMembersToValidate: number;
  numPotentialMembersToRemind: number;
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
  canViewMembers: boolean;
  city: string;
  cityCode: string;
  codeSafirPe: string;
  creationDate: string;
  department: string;
  email: string;
  fullDesc: string;
  hasAdmin: boolean;
  numAdmins: number;
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
  noDoraForm: boolean;
  numModels: number;
  numServices: number;
  openingHours: string | null;
  openingHoursDetails: string | null;
  otherLabels: string;
  parent: string;
  parentName: string;
  parentSiret: string;
  parentSlug: string;
  phone: string;
  postalCode: string;
  quickStartDone: boolean;
  services: StructureService[];
  shortAdminNames: string[];
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
  restrictedNationalLabels: NationalLabel[];
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
  | "adhesion";

export type SavedSearchNotificationFrequency =
  | "NEVER"
  | "TWO_WEEKS"
  | "MONTHLY";

export type CoachOrientationModes =
  | "formulaire-dora"
  | "completer-le-formulaire-dadhesion"
  | "envoyer-un-mail-avec-une-fiche-de-prescription"
  | "envoyer-un-mail"
  | "telephoner"
  | "autre";

export type BeneficiaryAccessModes =
  | "professionnel"
  | "se-presenter"
  | "completer-le-formulaire-dadhesion"
  | "envoyer-un-mail"
  | "telephoner"
  | "autre";

export type UpdateFrequency =
  | "tous-les-mois"
  | "tous-les-3-mois"
  | "tous-les-6-mois"
  | "tous-les-12-mois"
  | "tous-les-16-mois"
  | "jamais";

export interface FundingLabel {
  value: string;
  label: string;
}

export interface SearchQuery {
  categoryIds: string[];
  subCategoryIds: string[];
  cityCode: string;
  cityLabel: string;
  label?: string;
  kindIds: ServiceKind[];
  feeConditions: FeeCondition[];
  locationKinds: LocationKind[];
  fundingLabels: Array<FundingLabel["value"]>;
  lat?: number;
  lon?: number;
}

export type Coordinates = [longitude: number, latitude: number];

export interface ServiceSearchResult {
  // Une valeur nulle (null) signifie que l'information n'est pas renseignée tandis
  // qu'une valeur vide ("" ou []) signifie que l'information est renseignée mais vide.
  // Ces valeurs ayant un sens différent, leur traitement peut lui aussi différer.
  distance: number;
  address1: string;
  address2: string;
  postalCode: string;
  city: string;
  coordinates: Coordinates | null;
  diffusionZoneType: string;
  isOrientable?: boolean;
  coachOrientationModes?: string[];
  beneficiariesAccessModes?: string[];
  fundingLabels: Array<FundingLabel>;
  modificationDate: string;
  name: string;
  shortDesc: string;
  slug: string;
  structure: string;
  status: ServiceStatus;
  updateNeeded: boolean;
  kinds: ServiceKind[] | null;
  feeCondition: FeeCondition | null;
  locationKinds: LocationKind[];
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
  type?: "di";
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
  email: string;
  hasAdmin: boolean;
  name: string;
  numServices: number;
  phone: string;
  postalCode: string;
  shortDesc: string;
  siret: string;
  slug: string;
  url: string;
}

export interface Point {
  type: "Point";
  coordinates: Coordinates;
}

export interface Service {
  markSynced?: boolean;
  accessConditions: CustomizableFK[] | null;
  accessConditionsDisplay: string[] | null;
  address1: string;
  address2: string | null;
  addressLine: string;
  beneficiariesAccessModes: BeneficiaryAccessModes[] | null;
  beneficiariesAccessModesDisplay: string[] | null;
  beneficiariesAccessModesExternalFormLinkText: string;
  beneficiariesAccessModesExternalFormLink: string | null;
  beneficiariesAccessModesOther: string | null;
  canWrite: boolean;
  categories: ServiceCategory[];
  categoriesDisplay: string[];
  city: string;
  cityCode: string;
  coachOrientationModes: CoachOrientationModes[] | null;
  coachOrientationModesDisplay: string[] | null;
  coachOrientationModesExternalFormLinkText: string;
  coachOrientationModesExternalFormLink: string | null;
  coachOrientationModesOther: string | null;
  publics: CustomizableFK[] | null; // TODO: should be plural
  publicsDisplay: string[] | null;
  contactInfoFilled: boolean;
  contactEmail: string | null;
  contactName: string | null;
  contactPhone: string | null;
  creationDate: string | null;
  credentials: CustomizableFK[] | null;
  credentialsDisplay: string[] | null;
  department: string;
  diffusionZoneDetails: string;
  diffusionZoneDetailsDisplay: string;
  diffusionZoneType: AdminDivisionType;
  diffusionZoneTypeDisplay: string;
  durationWeeklyHours: number | null;
  durationWeeks: number | null;
  feeCondition: FeeCondition | null;
  feeDetails: string | null;
  fillingDuration?: number;
  forms: string[] | null;
  formsInfo: FileInfo[] | null;
  fullDesc: string;
  fundingLabels: Array<FundingLabel["value"]>;
  fundingLabelsDisplay: Array<FundingLabel["label"]>;
  geom: Point | null;
  hasAlreadyBeenUnpublished: boolean | null;
  isAvailable: boolean;
  isContactInfoPublic: boolean | null;
  isCumulative: boolean;
  isModel: false;
  isOrientable: boolean;
  kinds: ServiceKind[] | null;
  kindsDisplay: string[] | null;
  lienSource?: string | null;
  locationKinds: LocationKind[] | null;
  locationKindsDisplay: string[] | null;
  model: string | null;
  modelChanged: boolean | null;
  modificationDate: string | null;
  name: string;
  onlineForm: string | null;
  postalCode: string;
  publicationDate: string | null;
  qpvOrZrr: boolean | null;
  recurrence: string | null;
  remoteUrl: string | null;
  requirements: CustomizableFK[] | null;
  requirementsDisplay: string[] | null;
  shortDesc: string;
  slug: string;
  source?: string;
  status: ServiceStatus;
  structure: string;
  structureInfo: ServiceStructure;
  subcategories: string[];
  subcategoriesDisplay: string[];
  suspensionDate: string | null;
  useInclusionNumeriqueScheme: boolean;
  updateFrequency: UpdateFrequency | null;
  updateFrequencyDisplay: string | null;
  updateNeeded: boolean;
  isOrientableFtService: boolean;
}

export interface ShortService {
  categoriesDisplay: string[];
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
  locationKinds: LocationKind[];
  useInclusionNumeriqueScheme: boolean;
  updateNeeded: boolean;
}

export interface ShortBookmark {
  id: number;
  slug: string;
  creationDate: string;
  isDI: boolean;
}

export interface Bookmark {
  id: number;
  slug: string;
  creationDate: string;
  isDi: boolean;
  service: {
    name: string;
    structureName: string;
    structureSlug: string;
    postalCode: string;
    city: string;
    shortDesc: string;
    source: string;
  };
}

export interface SavedSearch {
  id: number;
  creationDate: string;
  cityCode: string;
  cityLabel: string;
  label: string;
  category: string;
  categoryDisplay: string;
  subcategories: string[];
  subcategoriesDisplay: string[];
  kinds: ServiceKind[];
  kindsDisplay: string[];
  fees: FeeCondition[];
  feesDisplay: string[];
  locationKinds: LocationKind[];
  locationKindsDisplay: string[];
  fundingLabels: FundingLabel["value"];
  fundingLabelsDisplay: FundingLabel["label"];
  frequency: SavedSearchNotificationFrequency;
  newServicesCount?: number;
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

  publics: CustomChoice[];
  credentials: CustomChoice[];
  deploymentDepartments: string[];
  diffusionZoneType: { value: AdminDivisionType; label: string }; // TODO: should be plural
  feeConditions: { value: FeeCondition; label: string }[];
  kinds: { value: ServiceKind; label: string }[];
  locationKinds: { value: LocationKind; label: string }[];
  requirements: CustomChoice[];
  subcategories: { value: string; label: string }[];
  updateFrequencies: { value: string; label: string }[];
};

export type Model = {
  accessConditions: CustomizableFK[];
  accessConditionsDisplay: string[];
  beneficiariesAccessModes: BeneficiaryAccessModes[];
  beneficiariesAccessModesDisplay: string[];
  beneficiariesAccessModesExternalFormLinkText: string;
  beneficiariesAccessModesExternalFormLink: string;
  beneficiariesAccessModesOther: string;
  canWrite: boolean;
  categories: ServiceCategory[];
  categoriesDisplay: string[];
  coachOrientationModes: CoachOrientationModes[];
  coachOrientationModesDisplay: string[];
  coachOrientationModesExternalFormLinkText: string;
  coachOrientationModesExternalFormLink: string;
  coachOrientationModesOther: string;
  publics: CustomizableFK[];
  publicsDisplay: string[];
  creationDate: string;
  credentials: CustomizableFK[];
  credentialsDisplay: string[];
  department: string;
  durationWeeklyHours: number;
  durationWeeks: number;
  externalFormLink: string;
  externalFormLinkText: string;
  feeCondition: FeeCondition;
  feeDetails: string;
  forms: string[];
  formsInfo: FileInfo[];
  fullDesc: string;
  fundingLabels: Array<FundingLabel["value"]>;
  fundingLabelsDisplay: Array<FundingLabel["label"]>;
  isCumulative: boolean;
  isModel: true;
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
  selectedLabel?: string;
  icon?: Component | null;
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

type ContactPreferences = "TELEPHONE" | "EMAIL" | "REFERENT" | "AUTRE";

export interface Orientation {
  // Tous les champs de l'étape 1 pouvant être optionnels
  // on est contraint de se baser sur un booléen pour s'assurer que l'étape 1 a bien été visionnée
  firstStepDone: boolean;
  contactBoxOpen: boolean;

  situation: string[];
  situationOther: string;
  requirements: string[];

  referentLastName: string;
  referentFirstName: string;
  referentPhone: string;
  referentEmail: string;
  prescriberStructureSlug: string;

  beneficiaryFranceTravailNumber: string;
  beneficiaryLastName: string;
  beneficiaryFirstName: string;
  beneficiaryAvailability: string | null;
  beneficiaryContactPreferences: ContactPreferences[];
  beneficiaryPhone: string;
  beneficiaryEmail: string;
  beneficiaryOtherContactMethod: string;
  orientationReasons: string;

  attachments: { [key: string]: string[] };

  dataProtectionCommitment: boolean;

  // Champs après la création de l'orientation
  id?: number;
  queryId: string;
  creationDate: string;
  prescriberStructure?: {
    name: string;
    slug: string;
  };
  processingDate?: string;
  status: "OUVERTE" | "VALIDÉE" | "REFUSÉE";
  beneficiaryAttachmentsDetails?: {
    name: string;
    url: string;
  }[];
  service?: {
    name: string;
    slug: string;
    contactName: string;
    contactPhone: string;
    contactEmail: string;
    structureName: string;
  };
  prescriber?: {
    name: string;
    email: string;
  };
}

export interface OrientationStats {
  totalSent: number;
  totalSentPending: number;
  totalReceived: number;
  totalReceivedPending: number;
}
