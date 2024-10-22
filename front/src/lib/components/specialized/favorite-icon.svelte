<script lang="ts">
  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import { createEventDispatcher } from "svelte";

  export let active = false;

  let disabled;
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
      title = "Connectez-vous pour ajouter<br/> ce service à vos favoris";
    } else if (active) {
      title = "Supprimer des favoris";
    } else {
      title = "Ajouter aux favoris";
    }
  }
</script>

<button
  class="tooltip icon inline-block h-s20 w-s20 shrink-0 fill-current text-gray-text-alt2 hover:text-magenta-cta print:hidden"
  class:active
  class:disabled
  aria-label={title}
  on:click={handleClick}
>
  {@html currentIcon}
  <div class="tooltiptext">{@html title}</div>
</button>

<style lang="postcss">
  .active {
    @apply text-magenta-cta;
  }

  .disabled {
    @apply text-gray-text-alt;
  }
  .tooltip {
    @apply relative inline-block print:hidden;
  }

  .tooltip .tooltiptext {
    @apply invisible absolute left-[-1000px] top-[-1000px] z-10 w-max -translate-x-1/2 rounded bg-magenta-dark px-s8 py-s2 text-center text-f12 font-bold text-white;
  }

  .tooltip .tooltiptext::after {
    content: "";
    @apply absolute bottom-full left-1/2 -ml-s4 border-4 border-solid border-transparent border-b-magenta-dark;
  }

  .tooltip:hover .tooltiptext,
  .tooltip:focus .tooltiptext {
    @apply visible left-1/2 top-s28 opacity-100;
  }
</style>
