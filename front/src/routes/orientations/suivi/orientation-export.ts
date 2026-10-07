import { generateSpreadsheet } from "$lib/utils/spreadsheet";
import type {
  OrientationExportData,
  OrientationExportType,
  ReceivedOrientationExportData,
  SentOrientationExportData,
} from "$lib/requests/orientations";

function formatSentOrientationExportData(
  exportData: Array<SentOrientationExportData>
) {
  return exportData.map((orientation) => ({
    "Envoyée le": orientation.creationDate,
    Statut: orientation.status,
    Bénéficiaire: orientation.beneficiaryName,
    "Structure concernée": orientation.structureName,
    "Service concerné": orientation.serviceName,
    Émetteur: orientation.prescriberName,
  }));
}

function formatReceivedOrientationExportData(
  exportData: Array<ReceivedOrientationExportData>
) {
  return exportData.map((orientation) => ({
    "Reçue le": orientation.creationDate,
    Source: orientation.source,
    Statut: orientation.status,
    Bénéficiaire: orientation.beneficiaryName,
    "Identifiant FT": orientation.beneficiaryFranceTravailNumber,
    "Service concerné": orientation.serviceName,
    "Structure émettrice": orientation.prescriberStructureName,
    "Contact émetteur": orientation.prescriberName,
    Lien: orientation.detailPageUrl,
  }));
}

export async function generateOrientationExport(
  structureSlug: string,
  type: OrientationExportType,
  exportData: OrientationExportData
) {
  const sheetData =
    type === "sent"
      ? formatSentOrientationExportData(
          exportData as Array<SentOrientationExportData>
        )
      : formatReceivedOrientationExportData(
          exportData as Array<ReceivedOrientationExportData>
        );

  const translatedType = type === "sent" ? "envoyees" : "recues";

  await generateSpreadsheet({
    sheetData,
    sheetName: `orientations-${translatedType}-dora-${structureSlug}`,
  });
}
