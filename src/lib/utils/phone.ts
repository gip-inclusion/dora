export function formatPhoneNumber(phoneNumber: string): string {
  return phoneNumber.match(/.{2}/g).join(" ");
}
