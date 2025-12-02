import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import { toast } from "@zerodevx/svelte-toast";
import { generateSpreadsheet } from "$lib/utils/spreadsheet";
import type { OrientationStats } from "$lib/types";
import { orientationState } from "./state.svelte";

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
  detailPageUrl: string;
}

async function fetchOrientationExportData(structureSlug: string) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export?type=${orientationState.selectedType}`;

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
    Lien: orientation.detailPageUrl,
  }));
}

export async function generateOrientationExport(structureSlug: string) {
  const exportData = await fetchOrientationExportData(structureSlug);

  let sheetData;

  if (!exportData) {
    toast.push("Une erreur est survenue lors de l’export des orientations.");
    return;
  }

  const type = orientationState.selectedType;

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

export function outputOrientationStats({
  totalSentPending,
  totalSent,
  totalReceivedPending,
  totalReceived,
}: OrientationStats) {
  if (orientationState.selectedType === "sent") {
    const pendingOrientations =
      totalSentPending > 1
        ? `${totalSentPending} demandes`
        : `${totalSentPending} demande`;

    const totalOrientations =
      totalSent > 1 ? `${totalSent} envoyées` : `${totalSent} envoyée`;

    return `<b>${pendingOrientations} en cours</b> / ${totalOrientations}`;
  }

  const pendingOrientations =
    totalSentPending > 1
      ? `${totalReceivedPending} demandes`
      : `${totalReceivedPending} demande`;

  const totalOrientations =
    totalReceived > 1 ? `${totalReceived} reçues` : `${totalReceived} reçue`;
  return `<b>${pendingOrientations} à traiter</b> / ${totalOrientations}`;
}
