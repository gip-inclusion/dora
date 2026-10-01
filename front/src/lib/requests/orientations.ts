import { getApiURL } from "$lib/utils/api";

export type OrientationExportType = "sent" | "received";

export interface SentOrientationExportData {
  creationDate: string;
  status: string;
  beneficiaryName: string;
  structureName: string;
  serviceName: string;
  prescriberName: string;
}

export interface ReceivedOrientationExportData extends Pick<
  SentOrientationExportData,
  | "creationDate"
  | "status"
  | "beneficiaryName"
  | "serviceName"
  | "prescriberName"
> {
  prescriberStructureName: string;
  detailPageUrl: string;
  source: string;
  beneficiaryFranceTravailNumber: string;
}

export type OrientationExportData = Array<
  SentOrientationExportData | ReceivedOrientationExportData
>;

export async function requestOrientationExportLink(
  structureSlug: string,
  type: OrientationExportType
) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export-link/`;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json; version=1.0",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ type }),
  });

  return { ok: response.ok, status: response.status };
}

export async function getOrientationExport(
  structureSlug: string,
  token: string
) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export/?token=${encodeURIComponent(token)}`;
  const response = await fetch(url, {
    headers: { Accept: "application/json; version=1.0" },
  });

  return {
    ok: response.ok,
    status: response.status,
    data: response.ok
      ? ((await response.json()) as OrientationExportData)
      : null,
  };
}
