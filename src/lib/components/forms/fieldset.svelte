<script>
  export let title = "";
  export let description = "";
  export let noTopPadding = false;
</script>

<div
  class="flex flex-col max-w-4xl gap-s24 pt-s32 mt-s48 bg-white rounded-md shadow-md px-s40 pb-s56 "
  class:no-top-padding={noTopPadding}
>
  <slot name="prefix" />
  {#if title}
    <div class="pb-s24 border-b border-gray-01">
      <h3 class="mb-s8 text-france-blue">
        {title}
      </h3>
      <slot name="description">
        {#if description}
          <p class="text-f14 text-gray-text-alt2">{description}</p>
        {/if}
      </slot>
    </div>
  {/if}
  <slot />
</div>

<style lang="postcss">
  .no-top-padding {
    @apply mt-s0;
  }
</style>
