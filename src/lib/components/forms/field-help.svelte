<script>
  import { lightBulbIcon } from "$lib/icons.js";
  export let title;
</script>

<style lang="postcss">
  .help {
    position: absolute;
    right: -472px;
    width: 384px;
  }

  .help-content :global(p) {
    @apply mb-s16 last:mb-s0;
  }
</style>

<div
  class="px-s16 pt-s16 pb-s24 bg-white border-l-s32 rounded-r help border-information"
>
  {#if title}
    <div
      class="flex font-bold flex-row items-center mb-s8 text-f17 leading-normal text-information"
    >
      <div class="w-s24 h-s24 mr-s8 fill-current">
        {@html lightBulbIcon}
      </div>
      {title}
    </div>
  {/if}
  <div class="help-content text-f14 leading-relaxed text-gray-text">
    <slot />
  </div>
</div>
