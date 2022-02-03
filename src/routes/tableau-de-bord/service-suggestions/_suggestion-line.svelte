<script>
  export let label;
  export let data;
  export let isList = false;
  export let verticalLayout = false;
  export let isBool = false;
</script>

<div
  class="flex flex-row"
  class:flex-col={verticalLayout}
  class:hidden={isList ? !data.length : !data}
>
  <div class="mr-s16 w-1/3 font-bold text-gray-text">{label}</div>
  <div class="text-gray-text">
    {#if isList}
      {#each data as item}
        <li>{item}</li>
      {/each}
    {:else}
      <slot>
        {#if isBool}
          {data ? "Oui" : "Non"}
        {:else}
          {data}
        {/if}
      </slot>
    {/if}
  </div>
</div>
