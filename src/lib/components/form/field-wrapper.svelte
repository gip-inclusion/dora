<script lang="ts">
  import Alert from "../forms/alert.svelte";

  export let label: string;
  export let name: string;
  export let helper = "";
  export let required = false;
  export let hidden = false;
  export let errorMessages: string[];
</script>

<div class="flex flex-col" class:hidden>
  <label
    class="bold mb-s8 font-bold text-gray-dark first-letter:capitalize"
    for={name}
  >
    {label}
    {#if required}
      <span class="text-error">*</span>
    {/if}
  </label>
  {#if helper}
    <p
      id="{name}-helper"
      class="helper m-s0 mb-s8 text-f12 text-gray-text-alt2"
    >
      {@html helper}
    </p>
  {/if}

  <slot />

  {#each errorMessages || [] as msg}
    <Alert id="{name}-error" label={msg} />
  {/each}
</div>

<style lang="postcss">
  .helper :global(a) {
    @apply text-magenta-cta underline;
  }
</style>
