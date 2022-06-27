<script>
  import { userInfo } from "$lib/auth";
  // import Input from "$lib/components/forms/input.svelte";
  // import Select from "$lib/components/forms/select.svelte";

  import LinkButton from "$lib/components/link-button.svelte";
  import ServiceCard from "$lib/components/services/service-card.svelte";
  import { SERVICE_STATUSES } from "$lib/schemas/service";

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

  function serviceOrder(se) {
    let ss = se
      .sort((a, b) => {
        if (order === "etat") {
          const sortOrder = {
            [SERVICE_STATUSES.suggestion]: 0,
            [SERVICE_STATUSES.draft]: 1,
            [SERVICE_STATUSES.published]: 2,
          };
          const orderA = sortOrder[a.status];
          const orderB = sortOrder[b.status];
          return orderA - orderB;
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
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <h2 class="text-france-blue">Services</h2>
  <div class="flex gap-s16">
    {#if !!services.length && !hasOptions}
      <LinkButton
        label={`Voir tous les services (${total})`}
        to="/structures/{structure.slug}/services"
        small
        secondary
      />
    {/if}
    {#if canEdit}
      <LinkButton
        label="Ajouter un service"
        to="/services/creer?structure={structure.slug}"
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
  {#each servicesOrdered as service}
    <ServiceCard {service} readOnly={!canEdit} {onRefresh} />
  {/each}
</div>
