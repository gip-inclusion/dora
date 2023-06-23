<script lang="ts">
  import LinkButton from "$lib/components/display/link-button.svelte";
  import ModelCard from "./model-card.svelte";
  import { copyIcon } from "$lib/icons";
  import Count from "../count.svelte";
  import NoModelNotice from "./no-model-notice.svelte";

  export let structure, models, total;
  export let tabDisplay = true;
  export let withEmptyNotice = false;
  export let limit;

  const orders = [
    { value: "date", label: "Date de mise à jour" },
    { value: "alpha", label: "Alphabétique" },
  ];

  const order = orders[0].value;
  let modelsOrdered;
  let filters;

  function modelsOrder(allModels) {
    let sortedModels = allModels
      .sort((a, b) => {
        if (order === "alpha") {
          return a.name.localeCompare(b.name, "fr", { numeric: true });
        }

        return new Date(b.modificationDate) - new Date(a.modificationDate);
      })
      .filter(
        (model) =>
          !filters ||
          filters
            .split(" ")
            .every((filter) =>
              model.name.toLowerCase().includes(filter.toLowerCase())
            )
      );

    if (limit) {
      sortedModels = sortedModels.slice(0, limit);
    }

    return sortedModels;
  }

  $: modelsOrdered = modelsOrder(models);
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <div class="flex flex-row gap-s8">
    <h2 class="mb-s0 text-france-blue">Modèles</h2>
    {#if limit}<Count>{total}</Count>{/if}
  </div>
  <div class="flex flex-wrap gap-s16">
    {#if !!models.length && !tabDisplay}
      <LinkButton
        label="Voir tous les modèles"
        to="/structures/{structure.slug}/modeles"
        small
        noBackground
      />
    {/if}
    {#if structure.canEditServices}
      <LinkButton
        label="Ajouter un modèle"
        icon={copyIcon}
        to="/modeles/creer?structure={structure.slug}"
      />
    {/if}
    <!-- {#if hasOptions}
      <div class="flex flex-col gap-s16 md:flex-row md:items-center">
        <div>Trier par</div>
        <div>
          <Select
            choices={orders}
            bind:value={order}
            initialValue={order}
            on:blur
            showClear={false}
          />
        </div>

        <Input type="text" bind:value={filters} placeholder="Mots-clé" />
      </div>
    {/if} -->
  </div>
</div>

{#if structure.isMember && modelsOrdered.length === 0 && withEmptyNotice}
  <NoModelNotice />
{:else}
  <div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-3">
    {#each modelsOrdered as model}
      <ModelCard {model} readOnly={!structure.canEditServices} />
    {/each}
  </div>
{/if}
