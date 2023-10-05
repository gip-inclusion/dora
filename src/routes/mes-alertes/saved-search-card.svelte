<script lang="ts">
  import DateLabel from "$lib/components/display/date-label.svelte";
  import { closeCircleIcon, historyLineIcon, mailLineIcon } from "$lib/icons";
  import type { SavedSearch } from "$lib/types";
  import {
    updateSavedSearchFrequency,
    deleteSavedSearch,
    getSavedSearchQueryString,
  } from "$lib/requests/saved-search";
  import { refreshUserInfo } from "$lib/utils/auth";
  import Button from "$lib/components/display/button.svelte";

  export let search: SavedSearch;

  let requesting = false;

  async function doDeleteAlert() {
    requesting = true;

    await deleteSavedSearch(search.id);
    await refreshUserInfo();

    requesting = false;
  }

  // Mise à jour de la fréquence d'envoi des alertes
  let frequencyValue = search.frequency;

  async function handleSubmit() {
    requesting = true;
    try {
      await updateSavedSearchFrequency(search.id, frequencyValue);
      await refreshUserInfo();
    } finally {
      requesting = false;
    }
  }
</script>

<div
  class="relative rounded-ml border border-gray-02 p-s32 pr-s56 shadow-sm"
  tabindex="-1"
>
  <h2 class="text-f20">
    <a href={`recherche?${getSavedSearchQueryString(search)}`}>
      Services d’insertion à proximité de {search.cityLabel}

      {#if search.category}
        pour la thématique {search.categoryDisplay}
      {/if}
    </a>
  </h2>

  <button
    class="absolute right-s32 top-s40 text-magenta-cta"
    disabled={requesting}
    on:click={doDeleteAlert}
  >
    <span
      class="mx-auto mb-s12 block h-s24 w-s24 fill-current"
      aria-label="Supprimer cette alerte"
    >
      {@html closeCircleIcon}
    </span>
  </button>

  {#if search.subcategories.length || search.kinds.length || search.fees.length}
    <p class="text-f16">
      {#if search.subcategories.length}
        Besoins sélectionnés : {search.subcategoriesDisplay.join(", ")}.
      {:else}
        Aucun besoin sélectionné.
      {/if}

      {#if search.kinds.length}
        Type de services : {search.kindsDisplay.join(", ")}.
      {/if}

      {#if search.fees.length}
        Frais à charge : {search.feesDisplay.join(", ")}.
      {/if}
    </p>
  {/if}

  <p class="text-f16">
    <span class="mr-s8 inline-block h-s16 w-s16 fill-current">
      {@html historyLineIcon}
    </span>
    Le <DateLabel date={search.creationDate} />
  </p>

  <div class="form-container">
    <form on:submit|preventDefault={handleSubmit} class="flex gap-s16">
      <div class="flex items-center rounded border border-gray-02 p-s12">
        <span class="mr-s8 inline-block h-s24 w-s24 fill-current">
          {@html mailLineIcon}
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
</div>
