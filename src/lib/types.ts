export type Structure = {
  name: string;
  slug: string;
  numServices: number;
};

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

  locationKinds: string[] | undefined;
  remoteUrl: string | undefined;
  postalCode: string | undefined;
  address1: string | undefined;
  address2: string | undefined;
  city: string | undefined;

  department: string;
  isAvailable: boolean;
  structureInfo: Structure;
  canWrite: boolean;
  structure: string;
  status: SERVICE_STATUSES;
  model: string | undefined;
  shortDesc: string | undefined;
  hasAlreadyBeenUnpublished: boolean;
  isCumulative: boolean;
  hasFee: boolean;
  feeDetails: string | undefined;
  recurrence: string | undefined;
  creationDate: string;
  modificationDate: string | undefined;
  diffusionZoneDetailsDisplay: string | undefined;
};
