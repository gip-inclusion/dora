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
  hasAlreadyBeenUnpublished: boolean;
  creationDate: string;
  name: string;
  slug: string;
  department: string;
  isAvailable: boolean;
  structureInfo: Structure;
  canWrite: boolean;
  structure: string;
  status: SERVICE_STATUSES;
  model: string | undefined;
  shortDesc: string | undefined;
  modificationDate: string | undefined;
  diffusionZoneDetailsDisplay: string | undefined;
};
