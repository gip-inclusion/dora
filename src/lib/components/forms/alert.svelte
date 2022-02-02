<script>
  import { alertIcon } from "$lib/icons.js";
  export let iconOnLeft = false,
    iconOnRight = false;
  export let label;
  export let isHTML = false;
</script>

<div class="text-error text-f12 flex flex-row items-center pt-s4">
  {#if iconOnLeft}
    <div class="w-s16 h-s16 mr-s8 fill-current">
      {@html alertIcon}
    </div>
  {/if}
  {#if isHTML}
    {@html label}
  {:else}
    {label}
  {/if}
  {#if iconOnRight}
    <div class="w-s16 h-s16 ml-s8 fill-current">
      {@html alertIcon}
    </div>
  {/if}
</div>
