<script>
  export let className = "";
  export let isDOMLabel = true;
</script>

{#if isDOMLabel}
  <!-- svelte-ignore a11y-label-has-associated-control -->
  <label class={className}>
    <slot />
  </label>
{:else}
  <div class={className}>
    <slot />
  </div>
{/if}
