<script>
  import { userInfo } from "$lib/auth";
  // import Input from "$lib/components/forms/input.svelte";
  // import Select from "$lib/components/forms/select.svelte";

  import LinkButton from "$lib/components/link-button.svelte";
  import ServiceCard from "$lib/components/services/service-card.svelte";

  export let structure, services, total;
  export let hasOptions = true;
  export let onRefresh;
  export let limit;
  let canEdit;

  const orders = [
    { value: "date", label: "Date de mise à jour" },
    { value: "alpha", label: "Alphabétique" },
    { value: "etat", label: "Publication" },
  ];
  const order = orders[0].value;
  let servicesOrdered;
  let filters;

  function serviceOrder() {
    let ss = services
      .sort((a, b) => {
        if (order === "etat") {
          if (
            (a.isSuggestion && b.isSuggestion) ||
            (!a.isSuggestion && a.isDraft && !b.isSuggestion && b.isDraft) ||
            (!a.isSuggestion && !a.isDraft && !b.isSuggestion && !b.isDraft)
          )
            return 0;

          if (a.isSuggestion) return 1;

          if (b.isSuggestion) return -1;

          if (!a.isSuggestion && !a.isDraft) return -1;

          if (!b.isSuggestion && !b.isDraft) return 1;

          return 0;
        }

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
  $: servicesOrdered = serviceOrder(services);

  async function handleRefresh() {
    if (onRefresh) {
      onRefresh();
    }
  }
</script>

<div class="col-span-full md:flex md:items-center md:justify-between">
  <h2 class="mb-s24 text-france-blue">Services</h2>
  <div class="flex gap-s16">
    {#if canEdit}
      <LinkButton
        label="Ajouter un service…"
        to="/services/creer?structure={structure.slug}"
        small
      />
    {/if}
    {#if !!services.length && !hasOptions}
      <LinkButton
        label={`Voir tous les services (${total})`}
        to="/structures/{structure.slug}/services"
        small
        secondary
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
<div class="col-span-full">
  <div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-4">
    {#each servicesOrdered as service}
      <ServiceCard {service} readOnly={!canEdit} onRefresh={handleRefresh} />
    {/each}
  </div>
</div>
