<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";

  import { userInfo } from "$lib/utils/auth";

  import Tooltip from "../ui/tooltip.svelte";

  export let active = false;

  const dispatch = createEventDispatcher();

  $: disabled = !$userInfo;

  function handleClick(evt: MouseEvent) {
    if (!disabled) {
      dispatch("click", evt);
    }
  }
</script>

<Tooltip>
  <button
    class="h-s20 w-s20 text-gray-text-alt2 hover:text-magenta-cta print:hidden"
    class:text-magenta-cta={active}
    class:text-gray-text-alt={disabled}
    on:click={handleClick}
  >
    {#if active}
      <BookmarkFillBusiness />
    {:else}
      <BookmarkLineBusiness />
    {/if}
  </button>
  <span slot="content">
    {#if disabled}
      Connectez-vous pour ajouter ce service à vos favoris
    {:else if active}
      Supprimer des favoris
    {:else}
      Ajouter aux favoris
    {/if}
  </span>
</Tooltip>
