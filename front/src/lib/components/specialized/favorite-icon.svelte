<script lang="ts">
  import { createEventDispatcher } from "svelte";

  import BookmarkFillBusiness from "svelte-remix/BookmarkFillBusiness.svelte";
  import BookmarkLineBusiness from "svelte-remix/BookmarkLineBusiness.svelte";

  import { userInfo } from "$lib/utils/auth";

  import Tooltip from "../ui/tooltip.svelte";

  interface Props {
    active?: boolean;
  }

  let { active = false }: Props = $props();

  const dispatch = createEventDispatcher();

  let disabled = $derived(!$userInfo);

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
    onclick={handleClick}
  >
    {#if active}
      <BookmarkFillBusiness />
    {:else}
      <BookmarkLineBusiness />
    {/if}
  </button>
  {#snippet content()}
    <span>
      {#if disabled}
        Connectez-vous pour ajouter ce service à vos favoris
      {:else if active}
        Supprimer des favoris
      {:else}
        Ajouter aux favoris
      {/if}
    </span>
  {/snippet}
</Tooltip>
