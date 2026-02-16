export function isOrphan(struct) {
  return struct.isOrphan;
}

export function isObsolete(struct) {
  return struct.isObsolete;
}

export function waiting(struct) {
  return struct.isWaiting;
}

export function adminAlreadyInvited(struct) {
  return struct.adminAlreadyInvited;
}

export function toModerate(struct) {
  return struct.awaitingModeration;
}

export function toActivate(struct) {
  return struct.awaitingActivation;
}

export function toUpdate(struct) {
  return struct.awaitingUpdate;
}
