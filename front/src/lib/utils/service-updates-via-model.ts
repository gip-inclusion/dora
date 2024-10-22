import { browser } from "$app/environment";
import dayjs from "dayjs";

const MODEL_NOTICES_HIDDEN_KEY = "structureModelNotices";

type StructureModelNotice = {
  slug: string;
  untilDate: string;
};

function getModelNotices(): StructureModelNotice[] {
  const data = window.localStorage.getItem(MODEL_NOTICES_HIDDEN_KEY) ?? "[]";

  try {
    return JSON.parse(data);
  } catch (_err) {
    return [];
  }
}

export function isModelNoticeHidden(structureSlug: string): boolean {
  if (!browser) {
    return true;
  }

  const structureModelNotice = getModelNotices().find(
    ({ slug }) => structureSlug === slug
  );

  if (!structureModelNotice) {
    return false;
  }

  return dayjs().isBefore(structureModelNotice.untilDate);
}

export function hideModelNotice(structureSlug: string): void {
  const modelNoticesWithoutStruct = getModelNotices().filter(
    ({ slug }) => structureSlug !== slug
  );

  window.localStorage.setItem(
    MODEL_NOTICES_HIDDEN_KEY,
    JSON.stringify([
      ...modelNoticesWithoutStruct,
      {
        slug: structureSlug,
        untilDate: dayjs().add(7, "day").startOf("day").toISOString(),
      },
    ])
  );
}

export function showModelNotice(structureSlug: string): void {
  window.localStorage.setItem(
    MODEL_NOTICES_HIDDEN_KEY,
    JSON.stringify(
      getModelNotices().filter(({ slug }) => structureSlug !== slug)
    )
  );
}
