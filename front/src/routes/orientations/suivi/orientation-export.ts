import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import type { OrientationType } from "./state.svelte";
import { toast } from "@zerodevx/svelte-toast";
import { generateSpreadsheet } from "$lib/utils/spreadsheet";

interface OrientationExportParams {
  structureSlug: string;
  type: OrientationType;
}

interface SentOrientationExportData {
  creationDate: string;
  status: string;
  beneficiaryName: string;
  structureName: string;
  serviceName: string;
  referentName: string;
}

async function fetchOrientationExportData({
  structureSlug,
  type,
}: OrientationExportParams) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export?type=${type}`;

  const result = await fetchData<Array<SentOrientationExportData>>(url);

  return result.data;
}

function formatSentOrientationExportData(
  exportData: Array<SentOrientationExportData>
) {
  return exportData.map((orientation) => ({
    "Envoyée le": orientation.creationDate,
    Statut: orientation.status,
    Bénéficiaire: orientation.beneficiaryName,
    "Structure concernée": orientation.structureName,
    "Service concerné": orientation.serviceName,
    Emetteur: orientation.referentName,
  }));
}

export async function generateOrientationExport(
  params: OrientationExportParams
) {
  const exportData = await fetchOrientationExportData(params);

  const { structureSlug, type } = params;

  let sheetData;

  if (!exportData) {
    toast.push(
      "Il y a eu une erreur en cherchant les données des orientations."
    );
    return;
  }

  if (type === "sent") {
    sheetData = formatSentOrientationExportData(exportData);
  }

  generateSpreadsheet<Array<SentOrientationExportData>>({
    sheetData,
    sheetName: `orientations-${type}-dora-${structureSlug}`,
  });
}
