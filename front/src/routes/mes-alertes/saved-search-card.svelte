<script lang="ts">
  import { preventDefault } from "svelte/legacy";

  import DateLabel from "$lib/components/display/date-label.svelte";
  import {
    closeCircleIcon,
    historyLineIcon,
    mailSendLineIcon,
  } from "$lib/icons";
  import type { SavedSearch } from "$lib/types";
  import {
    updateSavedSearchFrequency,
    deleteSavedSearch,
  } from "$lib/requests/saved-search";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SavedSearchDescription from "./description.svelte";
  import SavedSearchTitle from "./title.svelte";

  interface Props {
    search: SavedSearch;
    onDelete: (searchId: number) => void;
  }

  let { search = $bindable(), onDelete }: Props = $props();
  let requesting = $state(false);

  async function doDelete() {
    requesting = true;

    await deleteSavedSearch(search.id);
    if (onDelete) {
      onDelete(search.id);
    }

    requesting = false;
  }

  // Mise à jour de la fréquence d'envoi des alertes
  let frequencyValue = $state(search.frequency);

  async function handleSubmit() {
    requesting = true;
    try {
      await updateSavedSearchFrequency(search.id, frequencyValue);
      search.frequency = frequencyValue;
    } finally {
      requesting = false;
    }
  }

  $effect(() => {
    console.log(
      "frequencyValue !== search.frequency",
      frequencyValue,
      search.frequency
    );
  });
</script>

<div
  class="border-gray-02 p-s32 pr-s56 relative rounded-2xl border shadow-sm"
  tabindex="-1"
>
  <SavedSearchTitle {search} />

  <button
    class="right-s32 top-s40 text-magenta-cta absolute"
    disabled={requesting}
    onclick={doDelete}
  >
    <span
      class="mb-s12 h-s24 w-s24 mx-auto block fill-current"
      aria-label="Supprimer cette alerte"
    >
      {@html closeCircleIcon}
    </span>
  </button>

  <SavedSearchDescription {search} />

  <p class="text-f16">
    <span class="mr-s8 h-s16 w-s16 inline-block fill-current">
      {@html historyLineIcon}
    </span>
    Le <DateLabel date={search.creationDate} />
  </p>
  <div class="gap-s8 flex">
    <div class="form-container">
      <form onsubmit={preventDefault(handleSubmit)} class="gap-s16 flex">
        <div class="border-gray-02 p-s12 flex items-center rounded-sm border">
          <span class="mr-s8 h-s24 w-s24 inline-block fill-current">
            {@html mailSendLineIcon}
          </span>

          <select
            id="frequency"
            bind:value={frequencyValue}
            class="pr-s10 border-0"
          >
            <option value="NEVER">Pas de notification</option>
            <option value="TWO_WEEKS">Une alerte toutes les 2 semaines</option>
            <option value="MONTHLY">Une alerte tous les mois</option>
          </select>
        </div>

        {#if frequencyValue !== search.frequency}
          <Button
            name="validate"
            type="submit"
            label="Valider"
            disabled={requesting}
          />
        {/if}
      </form>
    </div>
    {#if search.newServicesCount}
      <LinkButton
        label={search.newServicesCount > 1
          ? `Voir les ${search.newServicesCount} nouveaux services`
          : "Voir le nouveau service"}
        to="/mes-alertes/{search.id}"
        secondary
      />{/if}
  </div>
</div>
