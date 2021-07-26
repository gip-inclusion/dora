<script>
  import { goto } from "$app/navigation";
  import { browser } from "$app/env";

  import { service } from "./_creation-store.js";

  import { storageKey } from "./_constants.js";
  import Validate from "./_validate.svelte";

  import arrowRightIcon from "remixicon/icons/System/arrow-right-line.svg?raw";
  import arrowLeftIcon from "remixicon/icons/System/arrow-left-line.svg?raw";

  export let previousLink, nextLink;
  export let withValidate = false;

  function persistStore() {
    if (browser) {
      localStorage.setItem(storageKey, JSON.stringify($service));
    }
  }

  function handleBackward() {
    persistStore();
    goto(previousLink);
  }

  function handleForward() {
    persistStore();
    goto(nextLink);
  }
</script>

<div class="flex flex-row justify-center max-w-xl gap-6 p-8 mx-auto mt-8">
  {#if previousLink}
    <button
      on:click|preventDefault={handleBackward}
      href={previousLink}
      class="flex flex-row p-2 px-4 text-center bg-white border-2 rounded text-action w-36 disabled:bg-back2 ">
      <div class="relative w-5 mr-3 fill-current top-1">
        {@html arrowLeftIcon}
      </div>
      <div>Précédent</div>
    </button>
  {/if}
  {#if nextLink}
    <button
      on:click|preventDefault={handleForward}
      href={nextLink}
      class="flex flex-row w-32 p-2 px-4 text-center text-white border-2 rounded bg-action disabled:bg-back2 ">
      <div>Suivant</div>
      <div class="relative w-5 ml-3 fill-current top-1">
        {@html arrowRightIcon}
      </div>
    </button>
  {/if}
  {#if withValidate}
    <Validate />
  {/if}
</div>
