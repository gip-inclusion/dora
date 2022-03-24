<script>
  import { informationIcon } from "$lib/icons.js";
  export let title;
  export let icon;
</script>

<div class="wrapper">
  {#if title}
    <div class="mb-s8 flex items-center text-f17 font-bold text-info">
      <div class="mr-s8 h-s24 w-s24 fill-current">
        {@html icon || informationIcon}
      </div>
      {title}
    </div>
  {/if}
  <div class="text-f14 leading-24 text-gray-text">
    <slot />
  </div>
</div>

<style lang="postcss">
  .wrapper {
    padding: var(--s16);
    margin: var(--s32) 0;
    background-color: var(--col-info-light);
    border-radius: var(--s4);
  }
</style>
