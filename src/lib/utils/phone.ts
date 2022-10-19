export function formatPhoneNumber(phoneNumber: string): string {
  try {
    return phoneNumber.match(/.{2}/g).join(" ");
  } catch {
    // On ne cherche pas à logguer l'erreur ici, ce sera fait
    // dans les scripts de nettoyage de la BDD
    return phoneNumber;
  }
}
