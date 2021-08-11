<script>
  export let title;
  export let description;
</script>

<div
  class="flex flex-col max-w-4xl gap-6 pt-4 mt-6 bg-white rounded-md shadow-sm px-7 pb-7 ">
  {#if title}
    <div class="border-gray-01 border-b pb-3">
      <h3 class="mb-1">
        {title}
      </h3>
      {#if description}
        <p class="text-gray-text-alt2 text-xs">{description}</p>
      {/if}
    </div>
  {/if}
  <slot />
</div>
