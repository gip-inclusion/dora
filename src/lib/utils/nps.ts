import dayjs from "dayjs";

// Un formulaire Tally ne sera pas réaffiché avant que
// `MIN_DAYS_BETWEEN_DISPLAYS` ne soient passés
const MIN_DAYS_BETWEEN_DISPLAYS = 30;

export enum TallyFormId {
  NPS_SEEKER_FORM_ID = "3xXVJ5",
  NPS_OFFEROR_FORM_ID = "3NpeZN",
  SERVICE_CREATION_FORM_ID = "mRGdpK",
}

interface TallyFormLocalStorageItem {
  lastSubmitted: string;
}

export function handleSubmitNpsForm(formId: TallyFormId): void {
  const key = getNpsAnswerLocalStorageKey(formId);
  const item: TallyFormLocalStorageItem = {
    lastSubmitted: dayjs().toString(),
  };
  localStorage.setItem(key, JSON.stringify(item));
}

export function canDisplayNpsForm(formId: TallyFormId): boolean {
  const key = getNpsAnswerLocalStorageKey(formId);
  const item = JSON.parse(localStorage.getItem(key));
  if (item && "lastSubmitted" in item) {
    const lastSubmitted = dayjs(item.lastSubmitted);
    if (lastSubmitted.isValid()) {
      const daysElapsed = dayjs().diff(lastSubmitted, "day");
      return daysElapsed > MIN_DAYS_BETWEEN_DISPLAYS;
    }
  }
  return true;
}

function getNpsAnswerLocalStorageKey(formId: TallyFormId): string {
  return `tallyForm-${formId}`;
}
