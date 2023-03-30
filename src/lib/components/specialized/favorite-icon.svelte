<script lang="ts">
  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import { createEventDispatcher } from "svelte";

  export let active = false;
  export let inverted = false;
  export let big = false;
  export let small = false;

  let title;

  const dispatch = createEventDispatcher();

  function handleClick(evt: MouseEvent) {
    if (!disabled) {
      dispatch("click", evt);
    }
  }

  $: currentIcon = active ? starSmileFillIcon : starSmileLineIcon;
  $: disabled = !$userInfo;
  $: {
    if (disabled) {
      title = "Connectez-vous";
    } else if (active) {
      title = "Supprimer des favoris";
    } else {
      title = "Ajouter aux favoris";
    }
  }
</script>

<button
  class="tooltip icon inline-block h-s24 w-s24 shrink-0 fill-current text-gray-text-alt2 hover:text-magenta-cta print:hidden"
  class:active
  class:inverted
  class:big
  class:small
  class:disabled
  aria-label={title}
  on:click={handleClick}
>
  {@html currentIcon}
  <div class="tooltiptext" aria-hidden="true">{title}</div>
</button>

<style lang="postcss">
  .active {
    @apply text-magenta-cta;
  }

  .inverted {
    @apply text-gray-01 hover:text-white;
  }

  .inverted.active {
    @apply text-white;
  }

  .big {
    @apply h-s24 w-s24 md:h-s32 md:w-s32;
  }

  .small {
    @apply h-s20 w-s20;
  }

  .disabled {
    @apply text-gray-text-alt;
  }

  .tooltip {
    @apply relative inline-block print:hidden;
  }

  .tooltip .tooltiptext {
    @apply invisible absolute top-[-1000px] left-[-1000px] z-10 w-max -translate-x-1/2 rounded bg-magenta-dark px-s8 py-s2 text-center text-f12 font-bold text-white;
  }

  .tooltip.big .tooltiptext {
    @apply top-s35;
  }

  .tooltip .tooltiptext::after {
    content: "";
    @apply absolute bottom-full left-1/2 -ml-s4 border-4 border-solid border-transparent border-b-magenta-dark;
  }

  .tooltip:hover .tooltiptext {
    @apply visible top-s28 left-1/2 opacity-100;
  }
</style>
