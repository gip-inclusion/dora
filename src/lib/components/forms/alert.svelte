<script>
  import { alertIcon } from "$lib/icons.js";
  export let label;
  export let isHTML = false;
</script>

<div class="flex flex-row items-center pt-s4 text-f12 text-error">
  <div class="mr-s8 h-s16 w-s16 fill-current">
    {@html alertIcon}
  </div>
  {#if isHTML}
    {@html label}
  {:else}
    {label}
  {/if}
</div>
