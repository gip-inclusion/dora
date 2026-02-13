export type NexusServiceID =
  | "dora"
  | "les-emplois"
  | "le-marche"
  | "mon-recap"
  | "pilotage";

export type NexusService = {
  id: NexusServiceID;
  label: string;
  url: string;
  icon: string;
};

export type NexusDropDownStatus = {
  proconnect: boolean;
  activated_services: NexusServiceID[];
  "mvp-enabled": boolean;
};
