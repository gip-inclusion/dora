<script>
  import { userInfo } from "$lib/auth";

  import Tabs from "$lib/components/tabs-light.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import ServiceCard from "$lib/components/services/service-card.svelte";
  import { SERVICE_STATUSES } from "$lib/schemas/service";

  export let structure, services, total, servicesOptions;
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
  let servicesDisplayed;
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

  let tabId = "default";

  async function handleTabChange(newTab) {
    tabId = newTab;
  }

  const tabs = [
    { id: "default", name: "Défaut" },
    { id: "archived", name: "Archivés" },
  ];

  $: canEdit = structure.isMember || $userInfo?.isStaff;
  $: servicesDisplayed = serviceOrder(services);
  $: {
    if (tabId === "archived") {
      services = structure.archivedServices;
    } else {
      services = structure.services;
    }
  }
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
  </div>
</div>
{#if hasOptions}
  <div
    class=" mb-s24 flex h-s72 flex-row items-center gap-s16 rounded-md bg-white px-s12 shadow-md"
  >
    <div class="text-f16 font-bold">Filtrer par&nbsp;:</div>
    <Tabs items={tabs} onSelectedChange={handleTabChange} itemId={tabId} />
  </div>
{/if}

<div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-4">
  {#each servicesDisplayed as service}
    <ServiceCard {service} {servicesOptions} readOnly={!canEdit} {onRefresh} />
  {/each}
</div>
