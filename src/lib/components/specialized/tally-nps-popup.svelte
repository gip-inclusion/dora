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
  export let timeoutSeconds;
  export let hiddenFields: Partial<HiddenFields> = {};

  let timeoutFn: ReturnType<typeof setTimeout>;

  onMount(() => {
    if (window.Tally) {
      window.Tally.closePopup(formId);
    }

    if (canDisplayNpsForm(formId)) {
      timeoutFn = setTimeout(() => {
        if (window.Tally) {
          window.Tally.openPopup(formId, {
            layout: "default",
            width: 420,
            hideTitle: true,
            hiddenFields,
            onClose: () => {
              saveNpsFormDateClosed(formId);
            },
            onSubmit: () => {
              saveNpsFormDateClosed(formId);
            },
          });
        }
      }, timeoutSeconds * 1000);
    }
  });

  onDestroy(() => {
    if (browser && window.Tally) {
      window.Tally.closePopup(formId);
    }

    clearTimeout(timeoutFn);
  });
</script>
