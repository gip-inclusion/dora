import dayjs from "dayjs";

// Un formulaire Tally ne sera pas réaffiché avant que
// `MIN_DAYS_BETWEEN_DISPLAYS` ne soient passés
const MIN_DAYS_BETWEEN_DISPLAYS = 14;

// eslint-disable-next-line no-shadow
export enum TallyFormId {
  NPS_FORM_ID = "nrDeXN",
  SERVICE_CREATION_FORM_ID = "mRGdpK",
}

export type HiddenFields = {
  user: "offreur" | "chercheur";
};

interface TallyFormLocalStorageItem {
  lastSubmitted: string;
}

function getNpsAnswerLocalStorageKey(formId: TallyFormId): string {
  return `tallyForm-${formId}`;
}

export function saveNpsFormDateClosed(formId: TallyFormId): void {
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
