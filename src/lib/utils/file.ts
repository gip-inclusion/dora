export function formatFilePath(filePath: string): string {
  const file = filePath.split("/").pop() as string;

  const dotPosition = file.lastIndexOf(".");
  if (dotPosition === -1) {
    return file;
  }

  const name = file.slice(0, dotPosition);
  const extension = file.slice(file.lastIndexOf("."), file.length);

  return `${name} (${extension})`;
}
