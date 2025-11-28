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

interface ReceivedOrientationExportData
  extends Pick<
    SentOrientationExportData,
    | "creationDate"
    | "status"
    | "beneficiaryName"
    | "serviceName"
    | "referentName"
  > {
  prescriberStructureName: string;
  serviceFrontendUrl: string;
}

async function fetchOrientationExportData({
  structureSlug,
  type,
}: OrientationExportParams) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export?type=${type}`;

  const result =
    await fetchData<
      Array<SentOrientationExportData | ReceivedOrientationExportData>
    >(url);

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
    Émetteur: orientation.referentName,
  }));
}

function formatReceivedOrientationExportData(
  exportData: Array<ReceivedOrientationExportData>
) {
  return exportData.map((orientation) => ({
    "Reçue le": orientation.creationDate,
    Statut: orientation.status,
    Bénéficiaire: orientation.beneficiaryName,
    "Service concerné": orientation.serviceName,
    "Structure émettrice": orientation.prescriberStructureName,
    "Contact émetteur": orientation.referentName,
    Lien: orientation.serviceFrontendUrl,
  }));
}

export async function generateOrientationExport(
  params: OrientationExportParams
) {
  const exportData = await fetchOrientationExportData(params);

  const { structureSlug, type } = params;

  let sheetData;

  if (!exportData) {
    toast.push("Une erreur est survenue lors de l’export des orientations.");
    return;
  }

  if (type === "sent") {
    sheetData = formatSentOrientationExportData(
      exportData as Array<SentOrientationExportData>
    );
  } else if (type === "received") {
    sheetData = formatReceivedOrientationExportData(
      exportData as Array<ReceivedOrientationExportData>
    );
  }

  const translatedType = type === "sent" ? "envoyees" : "recues";

  generateSpreadsheet<Array<SentOrientationExportData>>({
    sheetData,
    sheetName: `orientations-${translatedType}-dora-${structureSlug}`,
  });
}
