<script lang="ts">
  // Documentation : https://tally.so/help/popup-forms
  import { browser } from "$app/environment";
  import {
    canDisplayNpsForm,
    saveNpsFormDateClosed,
    type HiddenFields,
    type TallyFormId,
  } from "$lib/utils/nps";
  import { onDestroy, onMount } from "svelte";

  export let formId: TallyFormId;
  export let keySuffix = "";
  export let timeoutSeconds;
  export let hiddenFields: Partial<HiddenFields> = {};

  let timeoutFn: ReturnType<typeof setTimeout>;

  // Pour différencier un formulaire fermé par l'utilisateur vs un changement de page
  let tallyFormClosedByNavigation = false;

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

    if (canDisplayNpsForm(formId, keySuffix)) {
      timeoutFn = setTimeout(() => {
        if (window.Tally) {
          window.Tally.openPopup(formId, {
            layout: "default",
            width: 420,
            hideTitle: true,
            hiddenFields,
            onClose: () => {
              if (!tallyFormClosedByNavigation) {
                saveNpsFormDateClosed(formId, keySuffix);
              }
              tallyFormClosedByNavigation = false;
            },
            onSubmit: () => {
              saveNpsFormDateClosed(formId, keySuffix);
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
