<script>
  import { lightBulbIcon } from "$lib/icons.js";
  export let title;
</script>

<div
  class="help px-s16 pt-s16 pb-s24 bg-white border-l-4 rounded-r border-information"
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
  <div class="help-content">
    <slot />
  </div>
</div>

<style lang="postcss">
  .help {
    position: absolute;
    right: -472px;
    width: 384px;
  }

  .help-content,
  .help-content :global(p) {
    @apply mb-s16 last:mb-s0 text-f14 text-gray-text leading-relaxed;
  }
</style>
