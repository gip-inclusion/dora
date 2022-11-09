<script>
  import { onDestroy, onMount } from "svelte";
  import { browser } from "$app/env";
  import {
    getNpsAnswerLocalStorageKey,
    hasAnsweredNpsForm,
  } from "$lib/utils/nps";

  export let formId;
  export let timeout = 45000;
  const localStorageKey = getNpsAnswerLocalStorageKey(formId);
  export let hiddenFields = {};

  let timeoutFn;

  onMount(() => {
    if (window.Tally) window.Tally.closePopup(formId);
    const hasAnsweredForm = hasAnsweredNpsForm(formId);

    if (hasAnsweredForm) return;

    timeoutFn = setTimeout(() => {
      if (window.Tally) {
        window.Tally.openPopup(formId, {
          layout: "default",
          width: 420,
          hideTitle: true,
          autoClose: 0,
          hiddenFields,

          // Inspiré par : https://tally.so/help/popup-forms#f089d95828ef4e86a728611ded726822
          onSubmit: () => {
            localStorage.setItem(localStorageKey, "1");
          },
        });
      }
    }, timeout);
  });

  onDestroy(() => {
    if (browser && window.Tally) window.Tally.closePopup(formId);

    clearTimeout(timeoutFn);
  });
</script>
