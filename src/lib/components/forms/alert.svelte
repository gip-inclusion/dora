<script>
  import { alertIcon } from "$lib/icons.js";
  export let iconOnLeft = false,
    iconOnRight = false;
  export let label;
</script>

<div class="text-error text-xs flex flex-row items-center pt-1/2 ">
  {#if iconOnLeft}
    <div class="w-2 h-2 mr-1 fill-current ">
      {@html alertIcon}
    </div>
  {/if}
  {label}
  {#if iconOnRight}
    <div class="w-2 h-2 ml-1 fill-current">
      {@html alertIcon}
    </div>
  {/if}
</div>
