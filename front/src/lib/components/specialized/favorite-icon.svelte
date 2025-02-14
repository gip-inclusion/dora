<script lang="ts">
  import { run } from 'svelte/legacy';

  import { starSmileFillIcon, starSmileLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import { createEventDispatcher } from "svelte";

  interface Props {
    active?: boolean;
  }

  let { active = false }: Props = $props();

  let disabled = $state();
  let title = $state();

  const dispatch = createEventDispatcher();

  function handleClick(evt: MouseEvent) {
    if (!disabled) {
      dispatch("click", evt);
    }
  }

  let currentIcon = $derived(active ? starSmileFillIcon : starSmileLineIcon);
  run(() => {
    disabled = !$userInfo;
  });
  run(() => {
    if (disabled) {
      title = "Connectez-vous pour ajouter<br/> ce service à vos favoris";
    } else if (active) {
      title = "Supprimer des favoris";
    } else {
      title = "Ajouter aux favoris";
    }
  });
</script>

<button
  class="tooltip icon h-s20 w-s20 text-gray-text-alt2 hover:text-magenta-cta relative inline-block shrink-0 fill-current print:hidden"
  class:active
  class:disabled
  aria-label={title}
  onclick={handleClick}
>
  {@html currentIcon}
  <div
    class="tooltiptext bg-magenta-dark px-s8 py-s2 text-f12 invisible absolute top-[-1000px] left-[-1000px] z-10 w-max -translate-x-1/2 rounded-sm text-center font-bold text-white"
  >
    {@html title}
  </div>
</button>

<style lang="postcss">
  @reference "../../../app.css";

  .active {
    @apply text-magenta-cta;
  }

  .disabled {
    @apply text-gray-text-alt;
  }

  .tooltip .tooltiptext::after {
    content: "";
    @apply -ml-s4 border-b-magenta-dark absolute bottom-full left-1/2 border-4 border-solid border-transparent;
  }

  .tooltip:hover .tooltiptext,
  .tooltip:focus .tooltiptext {
    @apply top-s28 visible left-1/2 opacity-100;
  }
</style>
