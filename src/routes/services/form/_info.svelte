<script>
  import { informationIcon } from "$lib/icons.js";
  export let title;
  export let icon;
</script>

<div class="wrapper ">
  {#if title}
    <div class="flex text-f17 font-bold text-information mb-s8 items-center">
      <div class="w-s24 h-s24 mr-s8 fill-current">
        {@html icon || informationIcon}
      </div>
      {title}
    </div>
  {/if}
  <div class="text-gray-text text-f14 leading-24">
    <slot />
  </div>
</div>

<style>
  .wrapper {
    padding: var(--s16);
    margin: var(--s32) 0;
    background-color: var(--col-info-light);
    border-radius: var(--s4);
  }
</style>
