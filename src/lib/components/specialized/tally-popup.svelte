<script lang="ts">
  // Documentation : https://tally.so/help/popup-forms
  import dayjs from "dayjs";

  import { browser } from "$app/environment";
  import type { TallyFormId } from "$lib/consts";
  import { onDestroy, onMount } from "svelte";

  interface TallyFormLocalStorageItem {
    lastSubmitted: string;
  }
  type HiddenFields = {
    user: "offreur" | "chercheur";
  };

  // Un formulaire Tally ne sera pas réaffiché avant que
  // `MIN_DAYS_BETWEEN_DISPLAYS` ne soient passés
  const MIN_DAYS_BETWEEN_DISPLAYS = 30;

  export let formId: TallyFormId;
  export let keySuffix = "";
  export let timeoutSeconds: number;
  export let autoCloseSeconds = 0;
  export let hiddenFields: Partial<HiddenFields> = {};
  export let hideTitle = true;
  export let minDaysBetweenDisplays: number | null = MIN_DAYS_BETWEEN_DISPLAYS;

  let timeoutFn: ReturnType<typeof setTimeout>;

  // Pour différencier un formulaire fermé par l'utilisateur vs un changement de page
  let tallyFormClosedByNavigation = false;

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
            : daysElapsed > MIN_DAYS_BETWEEN_DISPLAYS;
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

<style lang="postcss">
  :global(.tally-popup) {
    @apply print:!hidden;
  }
</style>
