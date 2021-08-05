<script>
  import { externalLineIcon } from "$lib/icons";
  export let label = "";
  export let disabled;
  export let target;
  export let separator;
  export let external = false;
  export let light = false;
</script>

<button
  type="button"
  class="flex flex-row items-center justify-center py-2 text-sm text-center rounded outline-none  focus:shadow-focus"
  class:text-gray-text-alt2={light}
  class:text-gray-dark={!light}
  class:pr-4={!separator}
  on:click
  {disabled}>
  {label}
  {#if external}
    <div class="w-2 h-2 ml-1 fill-current">
      {@html externalLineIcon}
    </div>
  {/if}
  {#if separator}
    <div class="h-2 mx-2 border-l border-gray-03" />
  {/if}
</button>
