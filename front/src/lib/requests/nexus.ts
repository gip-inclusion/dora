import { getApiURL } from "$lib/utils/api";
import { getToken } from "$lib/utils/auth";

export type NexusServiceID =
  | "dora"
  | "les-emplois"
  | "le-marche"
  | "mon-recap"
  | "pilotage";

export type NexusMenuStatus = {
  proconnect: boolean;
  activatedServices: NexusServiceID[];
  enabled: boolean;
};

export const getNexusMenuStatus = async () => {
  const url = new URL("/nexus/menu-status/", getApiURL());
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${getToken()}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch Nexus menu status");
  }
  return response.json() as Promise<NexusMenuStatus>;
};
