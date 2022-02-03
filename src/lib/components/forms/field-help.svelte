<script>
  import { lightBulbIcon } from "$lib/icons.js";
  export let title;
</script>

<div
  class="help rounded-r border-l-4 border-information bg-white px-s16 pt-s16 pb-s24"
>
  {#if title}
    <div
      class="mb-s8 flex flex-row items-center text-f17 font-bold leading-normal text-information"
    >
      <div class="mr-s8 h-s24 w-s24 fill-current">
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
    @apply mb-s16 text-f14 leading-relaxed text-gray-text last:mb-s0;
  }
</style>
