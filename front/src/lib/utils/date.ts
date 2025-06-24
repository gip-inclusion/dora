export function formatNumericDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "numeric",
    year: "numeric",
  });
}
export function formatLongDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function toISODate(apiDate: string) {
  const date = new Date(apiDate);
  if (isNaN(date.getTime())) {
    return "";
  }
  const isoDateString = date.toISOString();
  return isoDateString.slice(0, isoDateString.indexOf("T"));
}

export function isLessThanOneHourAgo(dateString: string | null) {
  if (!dateString) {
    return false;
  }
  const date = new Date(dateString);
  const oneHourInMs = 60 * 60 * 1000;
  const oneHourAgo = new Date(Date.now() - oneHourInMs);
  return date > oneHourAgo;
}
