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
  mvpEnabled: boolean;
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

export type OrientationBeneficiaryInfo = {
  uid: string;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  franceTravailId: string;
};

export const getOrientationBeneficiaryInfo = async (jwt: string) => {
  const url = new URL("/nexus/orientation-beneficiary-info/", getApiURL());
  url.searchParams.set("jwt", jwt);

  const response = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${getToken()}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch orientation beneficiary info");
  }
  return response.json() as Promise<OrientationBeneficiaryInfo>;
};
