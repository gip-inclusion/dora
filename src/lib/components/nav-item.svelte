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
  class="flex flex-row items-center py-s8 text-f14 rounded outline-none"
  class:text-gray-text-alt2={light}
  class:text-gray-dark={!light}
  class:pr-s32={!separator}
  on:click
  {href}
  target="_blank"
  rel="noopener {nofollow ? 'nofollow' : ''}"
  {disabled}
>
  {label}
  {#if external}
    <div class="w-s16 h-s16 ml-s8 fill-current">
      {@html externalLineIcon}
    </div>
  {/if}
  {#if separator}
    <div class="h-s16 mx-s16 border-l border-gray-03" />
  {/if}
</a>
