<script lang="ts">
  interface Props {
    label: any;
    data: any;
    isList?: boolean;
    verticalLayout?: boolean;
    isBool?: boolean;
    children?: import("svelte").Snippet;
  }

  let {
    label,
    data,
    isList = false,
    verticalLayout = false,
    isBool = false,
    children,
  }: Props = $props();
</script>

<div
  class="flex flex-row"
  class:flex-col={verticalLayout}
  class:hidden={isList ? !data.length : !data}
>
  <div class="mr-s16 text-gray-text w-1/3 font-bold">{label}</div>
  <div class="text-gray-text">
    {#if isList}
      {#each data as item}
        <li>{item}</li>
      {/each}
    {:else if children}{@render children()}{:else if isBool}
      {data ? "Oui" : "Non"}
    {:else}
      {data}
    {/if}
  </div>
</div>
