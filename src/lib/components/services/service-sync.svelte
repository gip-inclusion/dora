<script>
  export let modelChanged = false;
  export let border = true;
</script>

<div
  class="flex text-f14 font-bold text-gray-text"
  class:border
  class:rounded={border}
  class:border-gray-01={border}
>
  <span class:px-s12={border} class:py-s6={border}>Synchronisé</span>

  {#if modelChanged}
    <span
      class="whitespace-nowrap text-warning"
      class:py-s6={border}
      class:pr-s8={border}
      class:ml-s12={!border}
    >
      Modèle mis à jour
    </span>
  {/if}

  {#if $$slots.default}
    <div class="py-s6 text-gray-02">|</div>
    <slot />
  {/if}
</div>
