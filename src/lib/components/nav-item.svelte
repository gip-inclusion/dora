<script>
  import { externalLinkIcon } from "$lib/icons";
  export let label = "";
  export let otherTab = false;
  export let disabled = false;
  export let separator = false;
  export let externalIcon = false;
  export let light = false;
  export let href;
  export let nofollow = false;
</script>

<a
  class="flex flex-row items-center rounded py-s8 text-f14 outline-none"
  class:text-gray-text-alt2={light}
  class:text-gray-dark={!light}
  class:pr-s32={!separator}
  on:click
  {href}
  target={otherTab ? "_blank" : ""}
  rel="noopener {nofollow ? 'nofollow' : ''}"
  {disabled}
>
  {label}
  {#if externalIcon}
    <div class="ml-s8 h-s16 w-s16 fill-current">
      {@html externalLinkIcon}
    </div>
  {/if}
  {#if separator}
    <div class="mx-s16 h-s16 border-l border-gray-03" />
  {/if}
</a>
