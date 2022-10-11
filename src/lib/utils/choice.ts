import type { Choice } from "$lib/types";

export function getChoiceFromValue(value: string, choices: Choice[]): Choice {
  return choices.find((c) => c.value === value);
}
export function getLabelFromValue(value: string, choices: Choice[]): string {
  return getChoiceFromValue(value, choices).label;
}
