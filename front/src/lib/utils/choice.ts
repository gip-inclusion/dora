import type { Choice } from "$lib/types";

export function getChoiceFromValue(value: string, choices: Choice[]): Choice {
  return choices.find((choice) => choice.value === value);
}
export function getLabelFromValue(value: string, choices: Choice[]): string {
  return getChoiceFromValue(value, choices).label;
}
export function getCategoryKeyFromSubcategoryChoice(choice: Choice): string {
  return choice.value.split("--")[0];
}
