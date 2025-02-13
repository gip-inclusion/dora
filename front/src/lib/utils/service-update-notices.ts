import { browser } from "$app/environment";
import dayjs from "dayjs";

export type NoticeType = "modelSync" | "update";

type StructureModelNotice = {
  slug: string;
  untilDate: string;
};

const HIDDEN_NOTICES_KEYS: Record<NoticeType, string> = {
  modelSync: "structureModelNotices",
  update: "updateNoticeHidden",
};

function getHiddenNotices(noticeType: NoticeType): StructureModelNotice[] {
  const data =
    window.localStorage.getItem(HIDDEN_NOTICES_KEYS[noticeType]) ?? "[]";

  try {
    return JSON.parse(data);
  } catch {
    return [];
  }
}

export function isNoticeHidden(
  noticeType: NoticeType,
  structureSlug: string
): boolean {
  if (!browser) {
    return true;
  }

  const hiddenNotices = getHiddenNotices(noticeType).find(
    ({ slug }) => structureSlug === slug
  );

  if (!hiddenNotices) {
    return false;
  }

  return dayjs().isBefore(hiddenNotices.untilDate);
}

export function hideNotice(
  noticeType: NoticeType,
  structureSlug: string
): void {
  const hiddenNoticesWithoutStruct = getHiddenNotices(noticeType).filter(
    ({ slug }) => structureSlug !== slug
  );

  window.localStorage.setItem(
    HIDDEN_NOTICES_KEYS[noticeType],
    JSON.stringify([
      ...hiddenNoticesWithoutStruct,
      {
        slug: structureSlug,
        untilDate: dayjs().add(7, "day").startOf("day").toISOString(),
      },
    ])
  );
}

export function showNotice(
  noticeType: NoticeType,
  structureSlug: string
): void {
  window.localStorage.setItem(
    HIDDEN_NOTICES_KEYS[noticeType],
    JSON.stringify(
      getHiddenNotices(noticeType).filter(({ slug }) => structureSlug !== slug)
    )
  );
}
