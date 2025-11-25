import * as XLSX from "xlsx";
import dayjs from "dayjs";

export function generateSpreadsheet<DATA extends Array<Record<string, any>>>({
  sheetData,
  sheetName,
}: {
  sheetData: DATA;
  sheetName: string;
}) {
  const numColumns = Object.keys(sheetData[0]).length;

  const worksheet = XLSX.utils.json_to_sheet(sheetData);
  worksheet["!cols"] = Array(numColumns).fill({ wch: 20 });
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet);
  const date = dayjs().format("YYYY-MM-DD");
  XLSX.writeFile(workbook, `${sheetName}-${date}.xlsx`, { compression: true });
}
