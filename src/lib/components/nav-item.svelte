<script>
  import { externalLineIcon } from "$lib/icons";
  export let label = "";
  export let disabled = false;
  export let separator = false;
  export let external = false;
  export let light = false;
  export let href;
  export let nofollow = false;
</script>

<a
  class="flex flex-row items-center py-1 text-sm rounded outline-none"
  class:text-gray-text-alt2={light}
  class:text-gray-dark={!light}
  class:pr-4={!separator}
  on:click
  {href}
  target="_blank"
  rel="noopener {nofollow ? 'nofollow' : ''}"
  {disabled}
>
  {label}
  {#if external}
    <div class="w-2 h-2 ml-1 fill-current">
      {@html externalLineIcon}
    </div>
  {/if}
  {#if separator}
    <div class="h-2 mx-2 border-l border-gray-03" />
  {/if}
</a>
