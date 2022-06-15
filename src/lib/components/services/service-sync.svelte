<script>
  import Tag from "../tag.svelte";

  export let modelChanged = false;
  export let border = true;
</script>

<div
  class="flex text-f14 font-bold text-gray-text"
  class:border
  class:rounded={border}
  class:border-gray-01={border}
>
  <div class="flex" class:px-s12={border} class:py-s6={border}>Synchronisé</div>

  {#if modelChanged}
    <div
      class="whitespace-nowrap"
      class:py-s6={border}
      class:pr-s8={border}
      class:ml-s12={!border}
    >
      <Tag bgColorClass="bg-warning">Modèle mis à jour</Tag>
    </div>
  {/if}

  {#if $$slots.default}
    <div class="py-s6 text-gray-02">|</div>
  {/if}
  <slot />
</div>
