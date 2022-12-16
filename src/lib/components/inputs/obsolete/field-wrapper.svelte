<script lang="ts">
  import Alert from "../../display/alert.svelte";

  export let label: string;
  export let name: string;
  export let helper = "";
  export let required = false;
  export let hidden = false;
  export let hideLabel = false;
  export let display: "horizontal" | "vertical" = "horizontal";
  export let errorMessages: string[] = [];
</script>

<div
  class="relative flex w-full {display === 'vertical'
    ? 'flex-row gap-s8'
    : 'flex-col'}"
  class:hidden
>
  <label
    class:sr-only={hideLabel}
    class="mb-s8  text-gray-dark {display}"
    for={name}
  >
    <h4 class="my-s4 first-letter:capitalize">{label}</h4>
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

  @screen lg {
    .vertical {
      @apply lg:w-1/4;
    }
  }
</style>
