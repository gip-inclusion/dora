import { fetchData } from "$lib/utils/misc";
import { getApiURL } from "$lib/utils/api";
import type { OrientationType } from "./state.svelte";
import * as XLSX from "xlsx";
import dayjs from "dayjs";

interface OrientationExportParams {
  structureSlug: string;
  type: OrientationType;
}

async function fetchOrientationExportData({
  structureSlug,
  type,
}: OrientationExportParams) {
  const url = `${getApiURL()}/structures/${structureSlug}/orientations/export?type=${type}`;

  const result = await fetchData(url);

  return result.data;
}

function formatSentOrientationExportData(exportData: any[]) {
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

  let sheetData;

  if (params.type === "sent") {
    sheetData = formatSentOrientationExportData(exportData);
  }

  const worksheet = XLSX.utils.json_to_sheet(sheetData);
  worksheet["!cols"] = Array(sheetData.keys().length).fill({ wch: 20 });
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet);
  const date = dayjs().format("YYYY-MM-DD");
  XLSX.writeFile(
    workbook,
    `orientations-sent-dora-${params.structureSlug}-${date}.xlsx`,
    { compression: true }
  );
}
