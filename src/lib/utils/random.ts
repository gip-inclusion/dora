import hexoid from "hexoid";

const generateId = hexoid();

export function randomId(): string {
  return generateId();
}
