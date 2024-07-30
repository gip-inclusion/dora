<script lang="ts">
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

  export let search: SavedSearch;
  export let onDelete: (searchId: number) => void;
  let requesting = false;

  async function doDelete() {
    requesting = true;

    await deleteSavedSearch(search.id);
    if (onDelete) {
      onDelete(search.id);
    }

    requesting = false;
  }

  // Mise à jour de la fréquence d'envoi des alertes
  let frequencyValue = search.frequency;

  async function handleSubmit() {
    requesting = true;
    try {
      await updateSavedSearchFrequency(search.id, frequencyValue);
      search.frequency = frequencyValue;
    } finally {
      requesting = false;
    }
  }
</script>

<div
  class="relative rounded-ml border border-gray-02 p-s32 pr-s56 shadow-sm"
  tabindex="-1"
>
  <SavedSearchTitle {search} />

  <button
    class="absolute right-s32 top-s40 text-magenta-cta"
    disabled={requesting}
    on:click={doDelete}
  >
    <span
      class="mx-auto mb-s12 block h-s24 w-s24 fill-current"
      aria-label="Supprimer cette alerte"
    >
      {@html closeCircleIcon}
    </span>
  </button>

  <SavedSearchDescription {search} />

  <p class="text-f16">
    <span class="mr-s8 inline-block h-s16 w-s16 fill-current">
      {@html historyLineIcon}
    </span>
    Le <DateLabel date={search.creationDate} />
  </p>
  <div class="flex gap-s8">
    <div class="form-container">
      <form on:submit|preventDefault={handleSubmit} class="flex gap-s16">
        <div class="flex items-center rounded border border-gray-02 p-s12">
          <span class="mr-s8 inline-block h-s24 w-s24 fill-current">
            {@html mailSendLineIcon}
          </span>

          <select
            id="frequency"
            bind:value={frequencyValue}
            class="border-0 pr-s10"
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
