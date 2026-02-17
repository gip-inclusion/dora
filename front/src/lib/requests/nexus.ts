import { getApiURL } from "$lib/utils/api";
import { getToken } from "$lib/utils/auth";

export type NexusServiceID =
  | "dora"
  | "les-emplois"
  | "le-marche"
  | "mon-recap"
  | "pilotage";

export type NexusDropDownStatus = {
  proconnect: boolean;
  activatedServices: NexusServiceID[];
  enabled: boolean;
};

export const getNexusDropdownStatus = async () => {
  const url = new URL("/nexus/dropdown-status/", getApiURL());
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${getToken()}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch Nexus dropdown status");
  }
  return response.json() as Promise<NexusDropDownStatus>;
};
