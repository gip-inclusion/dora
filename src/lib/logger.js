export function assert(condition, message) {
  if (!condition) {
    console.assert(message);
  }
}

export function logException(exc, ...args) {
  console.error(exc, ...args);
}
export function log(message, ...args) {
  console.log(message, ...args);
}
