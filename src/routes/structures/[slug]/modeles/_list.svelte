<script>
  import { userInfo } from "$lib/auth";
  // import Input from "$lib/components/forms/input.svelte";
  // import Select from "$lib/components/forms/select.svelte";

  import LinkButton from "$lib/components/link-button.svelte";
  import ModelCard from "$lib/components/services/model-card.svelte";

  export let structure, models, total;
  export let hasOptions = true;
  export let limit;
  let canEdit;

  const orders = [
    { value: "date", label: "Date de mise à jour" },
    { value: "alpha", label: "Alphabétique" },
  ];

  const order = orders[0].value;
  let modelsOrdered;
  let filters;

  function modelsOrder(se) {
    let ss = se
      .sort((a, b) => {
        if (order === "alpha") {
          return a.name.localeCompare(b.name, "fr", { numeric: true });
        }

        return new Date(b.modificationDate) - new Date(a.modificationDate);
      })
      .filter(
        (s) =>
          !filters ||
          filters
            .split(" ")
            .every((f) => s.name.toLowerCase().includes(f.toLowerCase()))
      );

    if (limit) {
      ss = ss.slice(0, limit);
    }

    return ss;
  }

  $: canEdit = structure.isMember || $userInfo?.isStaff;
  $: modelsOrdered = modelsOrder(models);
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <h2 class="text-france-blue">Modèles</h2>
  <div class="flex gap-s16">
    {#if !!models.length && !hasOptions}
      <LinkButton
        label={`Voir tous les modèles (${total})`}
        to="/structures/{structure.slug}/modeles"
        small
        secondary
      />
    {/if}
    {#if canEdit}
      <LinkButton
        label="Ajouter un modèle"
        to="/modeles/creer?structure={structure.slug}"
        small
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

<div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-4">
  {#each modelsOrdered as model}
    <ModelCard {model} readOnly={!canEdit} />
  {/each}
</div>
