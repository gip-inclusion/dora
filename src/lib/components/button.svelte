<script>
  export let label = "";
  export let icon;
  export let iconOnLeft;
  export let iconOnRight;
  export let type = "button";
  export let disabled;
</script>

<button
  {type}
  class="flex flex-row justify-center text-base leading-normal text-center text-white rounded py-3/2 px-5/2 bg-dora-magenta-cta hover:bg-dora-magenta-hover disabled:bg-gray-01 disabled:text-gray-text active:bg-france-blue "
  {disabled}>
  {#if iconOnLeft}
    <div class="w-3 h-3 mr-1 fill-current ">
      {@html icon}
    </div>
  {/if}
  {#if icon && !label}
    <div class="w-3 h-3 fill-current ">
      {@html icon}
    </div>
  {/if}
  {label}
  {#if iconOnRight}
    <div class="w-3 h-3 ml-1 fill-current">
      {@html icon}
    </div>
  {/if}
</button>
