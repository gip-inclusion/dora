<script lang="ts">
  // Documentation : https://tally.so/help/popup-forms
  import dayjs from "dayjs";

  import { browser } from "$app/environment";
  import type { TallyFormId } from "$lib/consts";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";

  interface TallyFormLocalStorageItem {
    lastSubmitted: string;
  }
  type HiddenFields = {
    source?: string;
    user: "offreur" | "chercheur";
  };

  // Un formulaire Tally ne sera pas réaffiché avant que
  // `MIN_DAYS_BETWEEN_DISPLAYS` ne soient passés
  const MIN_DAYS_BETWEEN_DISPLAYS = 30;

  interface Props {
    formId: TallyFormId;
    keySuffix?: string;
    timeoutSeconds: number;
    autoCloseSeconds?: number;
    hiddenFields?: Partial<HiddenFields>;
    hideTitle?: boolean;
    minDaysBetweenDisplays?: number | null;
  }

  let {
    formId,
    keySuffix = "",
    timeoutSeconds,
    autoCloseSeconds = 0,
    hiddenFields = {},
    hideTitle = true,
    minDaysBetweenDisplays = MIN_DAYS_BETWEEN_DISPLAYS
  }: Props = $props();

  let timeoutFn: ReturnType<typeof setTimeout>;

  // Pour différencier un formulaire fermé par l'utilisateur vs un changement de page
  let tallyFormClosedByNavigation = false;

  const dispatch = createEventDispatcher();

  function getTallyAnswerLocalStorageKey(): string {
    let key = `tallyForm-${formId}`;
    if (keySuffix) {
      key = `${key}-${keySuffix}`;
    }

    return key;
  }

  function saveClosureDate(): void {
    const key = getTallyAnswerLocalStorageKey();
    const item: TallyFormLocalStorageItem = {
      lastSubmitted: dayjs().toString(),
    };
    localStorage.setItem(key, JSON.stringify(item));
  }

  function canDisplayForm(): boolean {
    const key = getTallyAnswerLocalStorageKey();
    const value = localStorage.getItem(key);
    if (value) {
      const item = JSON.parse(value);
      if (item && "lastSubmitted" in item) {
        const lastSubmitted = dayjs(item.lastSubmitted);
        if (lastSubmitted.isValid()) {
          const daysElapsed = dayjs().diff(lastSubmitted, "day");
          return minDaysBetweenDisplays == null
            ? false
            : daysElapsed >= minDaysBetweenDisplays;
        }
      }
    }
    return true;
  }

  onMount(() => {
    if (!window.Tally) {
      // Chargement dynamique de Tally
      const tallyScript = window.document.createElement("script");
      tallyScript.setAttribute("src", "https://tally.so/widgets/embed.js");
      document.head.appendChild(tallyScript);
    } else {
      // On ferme une éventuelle popup en cours d'affichage
      window.Tally.closePopup(formId, keySuffix);
    }

    if (canDisplayForm()) {
      timeoutFn = setTimeout(() => {
        if (window.Tally) {
          window.Tally.openPopup(formId, {
            layout: "default",
            width: 440,
            autoClose: autoCloseSeconds || undefined,
            hideTitle,
            hiddenFields,
            emoji: {
              text: "👋",
              animation: "wave",
            },
            onClose: () => {
              if (!tallyFormClosedByNavigation) {
                saveClosureDate();
              }
              tallyFormClosedByNavigation = false;
            },
            onSubmit: () => {
              saveClosureDate();
              dispatch("submit");
            },
          });
        }
      }, timeoutSeconds * 1000);
    }
  });

  onDestroy(() => {
    if (browser && window.Tally) {
      tallyFormClosedByNavigation = true;
      window.Tally.closePopup(formId);
    }

    clearTimeout(timeoutFn);
  });
</script>
