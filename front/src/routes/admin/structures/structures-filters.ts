export function isOrphan(struct) {
  return !struct.hasAdmin && !struct.adminsToRemind.length;
}
export function isObsolete(struct) {
  return struct.isObsolete;
}
export function waiting(struct) {
  return struct.adminsToRemind.length;
}

export function toModerate(struct) {
  return struct.moderationStatus !== "VALIDATED";
}

export function toActivate(struct) {
  return !struct.numPublishedServices;
}

export function toUpdate(struct) {
  return struct.numOutdatedServices;
}
