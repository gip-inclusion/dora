<script lang="ts">
  import FileCopyLineDocument from "svelte-remix/FileCopyLineDocument.svelte";

  import LinkButton from "$lib/components/display/link-button.svelte";

  import ModelCard from "./model-card.svelte";
  import Count from "../count.svelte";
  import NoModelNotice from "./no-model-notice.svelte";

  interface Props {
    structure: any;
    models: any;
    total: any;
    tabDisplay?: boolean;
    withEmptyNotice?: boolean;
    limit: any;
  }

  let {
    structure,
    models,
    total,
    tabDisplay = true,
    withEmptyNotice = false,
    limit,
  }: Props = $props();

  const orders = [
    { value: "date", label: "Date de mise à jour" },
    { value: "alpha", label: "Alphabétique" },
  ];

  const order = orders[0].value;

  function modelsOrder(allModels) {
    let sortedModels = allModels.sort((a, b) => {
      if (order === "alpha") {
        return a.name.localeCompare(b.name, "fr", { numeric: true });
      }

      return new Date(b.modificationDate) - new Date(a.modificationDate);
    });

    if (limit) {
      sortedModels = sortedModels.slice(0, limit);
    }

    return sortedModels;
  }

  let modelsOrdered = $derived(modelsOrder(models));
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <div class="gap-s8 flex flex-row">
    <h2 class="mb-s0 text-france-blue">Modèles</h2>
    {#if limit}<Count>{total}</Count>{/if}
  </div>
  <div class="gap-s16 flex flex-wrap">
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
        icon={FileCopyLineDocument}
        to="/modeles/creer?structure={structure.slug}"
      />
    {/if}
  </div>
</div>

{#if structure.isMember && modelsOrdered.length === 0 && withEmptyNotice}
  <NoModelNotice />
{:else}
  <div class="mb-s48 gap-s16 grid md:grid-cols-2 lg:grid-cols-3">
    {#each modelsOrdered as model}
      <ModelCard {model} readOnly={!structure.canEditServices} />
    {/each}
  </div>
{/if}
