import dayjs from "dayjs";

export async function generateSpreadsheet<
  DATA extends Array<Record<string, any>>,
>({ sheetData, sheetName }: { sheetData: DATA; sheetName: string }) {
  // Import dynamique pour charger la lib uniquement côté navigateur et au moment de l'export
  const { default: writeExcelFile } = await import("write-excel-file/browser");

  const columns = Object.keys(sheetData[0]).map((header) => ({
    header,
    width: 20,
    cell: (row: DATA[number]) => ({ value: row[header] }),
  }));

  const date = dayjs().format("YYYY-MM-DD");
  await writeExcelFile(sheetData, { columns }).toFile(
    `${sheetName}-${date}.xlsx`
  );
}
