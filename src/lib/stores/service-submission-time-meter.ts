import type { Writable } from "svelte/store";
import { writable } from "svelte/store";

type FormTrackValues = {
  id: string | null; // slug or uuid
  duration: number | null; // in seconds
  showFeedbackModal: boolean;
};

type FormTrack = {
  subscribe: Writable<FormTrackValues>["subscribe"];

  incrementDuration: () => void;
  setId: (slug: string) => void;
  enableFeedbackModal: () => void;
  clear: () => void;
};

function createFormTrack(): FormTrack {
  const { subscribe, set, update }: Writable<FormTrackValues> = writable({
    id: null,
    duration: null,
    showFeedbackModal: false,
  });

  return {
    subscribe,

    /**
     * Add one second to duration
     */
    incrementDuration() {
      update((s) => ({
        ...s,
        duration: s.duration ? s.duration + 1 : 1,
      }));
    },

    setId(id: string) {
      update((s) => ({
        ...s,
        id,
      }));
    },

    enableFeedbackModal() {
      update((s) => ({
        ...s,
        showFeedbackModal: true,
      }));
    },

    clear: () =>
      set({
        id: null,
        duration: null,
        showFeedbackModal: true,
      }),
  };
}

export const serviceSubmissionTimeMeter = createFormTrack();
