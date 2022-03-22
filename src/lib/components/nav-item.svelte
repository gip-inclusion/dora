<script>
  import { externalLinkIcon } from "$lib/icons";
  export let label = "";
  export let otherTab = false;
  export let disabled = false;
  export let externalIcon = false;
  export let light = false;
  export let href;
  export let nofollow = false;
</script>

<a
  class="flex flex-row justify-between py-s8 text-f14 lg:items-center lg:pr-s32"
  class:text-gray-text-alt2={light}
  class:text-gray-dark={!light}
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
</a>
