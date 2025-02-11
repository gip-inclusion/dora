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
  class="tooltip icon h-s20 w-s20 text-gray-text-alt2 hover:text-magenta-cta inline-block shrink-0 fill-current print:hidden"
  class:active
  class:disabled
  aria-label={title}
  on:click={handleClick}
>
  {@html currentIcon}
  <div class="tooltiptext">{@html title}</div>
</button>

<style lang="postcss">
  @reference "../../../app.css";

  .active {
  }

  .disabled {
  }
  .tooltip {
  }

  .tooltip .tooltiptext {
  }

  .tooltip .tooltiptext::after {
    content: "";
  }

  .tooltip:hover .tooltiptext,
  .tooltip:focus .tooltiptext {
  }
</style>
