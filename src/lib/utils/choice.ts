import type { Choice } from "$lib/types";

export function getLabelFromValue(value: string, choices: Choice[]): string {
  return choices.find((c) => c.value === value).label;
}
