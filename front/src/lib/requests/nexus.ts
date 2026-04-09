import { toast } from "@zerodevx/svelte-toast";
import { ORIENTATION_JWT_QUERY_PARAM } from "$lib/consts";
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

type OrientationBeneficiaryInfoData = {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  franceTravailId: string;
};

type OrientationBeneficiaryInfoRedirect = {
  nextUrl: string;
};

export type OrientationBeneficiaryInfo =
  | OrientationBeneficiaryInfoData
  | OrientationBeneficiaryInfoRedirect;

export const getOrientationBeneficiaryInfo = async (
  opJwt: string,
  serviceSlug: string
) => {
  const url = new URL("/orientations/emplois/beneficiary-info/", getApiURL());
  url.searchParams.set(ORIENTATION_JWT_QUERY_PARAM, opJwt);
  url.searchParams.set("service_slug", serviceSlug);

  const response = await fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json; version=1.0",
      Authorization: `Token ${getToken()}`,
    },
  });

  if (!response.ok) {
    const body = await response.json();
    const errorDetails =
      body.op && body.op.length > 0 ? body.op[0].message : "";
    toast.push(
      "Une erreur est survenue lors de la récupération des informations du bénéficiaire" +
        (errorDetails ? ` : ${errorDetails}` : "")
    );
    throw new Error("Failed to fetch orientation beneficiary info");
  }

  return response.json() as Promise<OrientationBeneficiaryInfo>;
};
