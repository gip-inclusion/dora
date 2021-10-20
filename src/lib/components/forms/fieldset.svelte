<script>
  export let title = "";
  export let description = "";
  export let noTopPadding = false;
</script>

<style lang="postcss">
  .no-top-padding {
    @apply mt-0;
  }
</style>

<div
  class="flex flex-col max-w-4xl gap-3 pt-4 mt-6 bg-white rounded-md shadow-md px-5 pb-7 "
  class:no-top-padding={noTopPadding}>
  {#if title}
    <div class="pb-3 border-b border-gray-01">
      <h3 class="mb-1 text-france-blue">
        {title}
      </h3>
      <slot name="description">
        {#if description}
          <p class="text-sm text-gray-text-alt2">{description}</p>
        {/if}
      </slot>
    </div>
  {/if}
  <slot />
</div>
