export function getFileNameFromPath(filePath: string): string {
  return filePath.split("/").pop() ?? "";
}

// Reproduit `django.utils.text.get_valid_filename` : le serveur range les documents sous
// une clé dérivée du nom nettoyé (« mon dossier.pdf » devient « mon_dossier.pdf »), c’est
// donc sur ce nom-là que se joue la collision entre deux fichiers.
export function toValidFileName(fileName: string): string {
  return fileName
    .trim()
    .replace(/ /gu, "_")
    .replace(/[^-\p{L}\p{N}_.]/gu, "");
}

export function formatFilePath(filePath: string): string {
  const file = getFileNameFromPath(filePath);

  const dotPosition = file.lastIndexOf(".");
  if (dotPosition === -1) {
    return file;
  }

  const name = file.slice(0, dotPosition);
  const extension = file.slice(file.lastIndexOf("."), file.length);

  return `${name} (${extension})`;
}
