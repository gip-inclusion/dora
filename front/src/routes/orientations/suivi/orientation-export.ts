import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import { toast } from "@zerodevx/svelte-toast";
import { generateSpreadsheet } from "$lib/utils/spreadsheet";
import { orientationState } from "./state.svelte";

interface SentOrientationExportData {
  creationDate: string;
  status: string;
  beneficiaryName: string;
  structureName: string;
  serviceName: string;
  prescriberName: string;
}

interface ReceivedOrientationExportData extends Pick<
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

async function fetchOrientationExportData(structureSlug: string) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export?type=${orientationState.selectedType}`;

  const result =
    await fetchData<
      Array<SentOrientationExportData | ReceivedOrientationExportData>
    >(url);

  return result.data;
}

const FALLBACK_TEXT = "N/A";

// Remplace les valeurs vides (null, undefined ou chaîne vide) par FALLBACK_TEXT
function withFallbacks<T extends Record<string, unknown>>(row: T) {
  return Object.fromEntries(
    Object.entries(row).map(([key, value]) => [
      key,
      value == null || value === "" ? FALLBACK_TEXT : value,
    ])
  ) as { [K in keyof T]: T[K] | typeof FALLBACK_TEXT };
}

function formatSentOrientationExportData(
  exportData: Array<SentOrientationExportData>
) {
  return exportData.map((orientation) =>
    withFallbacks({
      "Envoyée le": orientation.creationDate,
      Statut: orientation.status,
      Bénéficiaire: orientation.beneficiaryName,
      "Structure concernée": orientation.structureName,
      "Service concerné": orientation.serviceName,
      Émetteur: orientation.prescriberName,
    })
  );
}

function formatReceivedOrientationExportData(
  exportData: Array<ReceivedOrientationExportData>
) {
  return exportData.map((orientation) =>
    withFallbacks({
      "Reçue le": orientation.creationDate,
      Statut: orientation.status,
      Bénéficiaire: orientation.beneficiaryName,
      "Identifiant FT": orientation.beneficiaryFranceTravailNumber,
      "Service concerné": orientation.serviceName,
      "Structure émettrice": orientation.prescriberStructureName,
      "Contact émetteur": orientation.prescriberName,
      Source: orientation.source,
      Lien: orientation.detailPageUrl,
    })
  );
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
