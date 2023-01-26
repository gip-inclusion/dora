import type { Choice } from "$lib/types";

export function getChoiceFromValue(value: string, choices: Choice[]): Choice {
  return choices.find((choice) => choice.value === value);
}
export function getLabelFromValue(value: string, choices: Choice[]): string {
  return getChoiceFromValue(value, choices).label;
}
export function getChoicesFromKey(key: string, choices: Choice[]) {
  const results = choices.filter((choice) => choice.value.startsWith(key));

  return results;
}
export function getCategoryKeyFromSubcategoryChoice(choice: Choice): string {
  return choice.value.split("--")[0];
}
export function injectOptGroupInSubCategories(choices: Choice[]): Choice[] {
  choices.forEach((choice) => {
    choice.optGroupKey = getCategoryKeyFromSubcategoryChoice(choice);
  });
  return choices;
}

export function injectOptGroupAllOptionsInSubCategories(
  optGroups: Choice[],
  choices: Choice[],
  allOptionLabel = "Tous"
) {
  return [
    ...choices,
    ...optGroups.map((optGroup: Choice) => ({
      value: `${optGroup.value}--all`,
      label: allOptionLabel,
      optGroupKey: optGroup.value,
      icon: optGroup.icon,
      selectedLabel: optGroup.label,
    })),
  ];
}
