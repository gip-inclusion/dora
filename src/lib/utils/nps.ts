export function hasAnsweredNpsForm(formId: string): boolean {
  const key = getNpsAnswerLocalStorageKey(formId);
  return !!localStorage.getItem(key);
}

export function getNpsAnswerLocalStorageKey(formId: string): string {
  return `popup_${formId}`;
}
