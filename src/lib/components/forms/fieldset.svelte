<script>
  export let title = "";
  export let description = "";
  export let noTopPadding = false;
</script>

<div
  class="mt-s48 flex max-w-4xl flex-col gap-s24 rounded-md bg-white px-s40 pt-s32 pb-s56 shadow-md "
  class:no-top-padding={noTopPadding}
>
  <slot name="prefix" />
  {#if title}
    <div class="border-b border-gray-01 pb-s24">
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
