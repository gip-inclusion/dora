<script>
  export let title;
  export let description;
</script>

<div
  class="flex flex-col max-w-4xl gap-4 pt-4 mt-6 bg-white rounded-md shadow-sm px-7 pb-7 ">
  {#if title}
    <div class="pb-3 border-b border-gray-01">
      <h3 class="mb-1">
        {title}
      </h3>
      {#if description}
        <p class="text-xs text-gray-text-alt2">{description}</p>
      {/if}
    </div>
  {/if}
  <slot />
</div>
