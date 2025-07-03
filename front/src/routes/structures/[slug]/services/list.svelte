<script lang="ts">
  import { run } from 'svelte/legacy';

  import { browser } from "$app/environment";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SelectField from "$lib/components/inputs/obsolete/select-field.svelte";
  import {
    addIcon,
    alertIcon,
    arrowDownLineIcon,
    arrowUpLineIcon,
    draftFillIcon,
    earthFillIcon,
    errorWarningIcon,
    fileEditFillIcon,
    folderFillIcon,
  } from "$lib/icons";
  import type { Choice, ServiceStatus, ShortService } from "$lib/types";
  import Count from "../count.svelte";
  import {
    hasArchivedServices,
    hasAtLeastOneServiceNotArchived,
  } from "../quick-start";
  import NoServiceNotice from "./no-service-notice.svelte";
  import ServiceCard from "./service-card.svelte";
  import ServicesToSyncWithModelNotice from "./services-to-sync-with-model-notice.svelte";
  import ServicesToUpdateNotice from "./services-to-update-notice.svelte";


  interface Props {
    structure: any;
    total: any;
    servicesOptions: any;
    tabDisplay?: boolean;
    onRefresh: any;
    limit?: number | undefined;
    withEmptyNotice?: boolean;
    serviceStatus: ServiceStatus | null;
    updateNeeded: "true" | "false" | null;
    servicesDisplayed?: ShortService[];
  }

  let {
    structure,
    total,
    servicesOptions,
    tabDisplay = true,
    onRefresh,
    limit = undefined,
    withEmptyNotice = false,
    serviceStatus = $bindable(),
    updateNeeded = $bindable(),
    servicesDisplayed = $bindable([])
  }: Props = $props();

  function updateUrlQueryParams() {
    if (!browser) {
      return;
    }

    const searchParams = $page.url.searchParams;

    if (serviceStatus) {
      searchParams.set("service-status", encodeURIComponent(serviceStatus));
    } else {
      searchParams.delete("service-status");
    }

    if (updateNeeded) {
      searchParams.set("update-needed", updateNeeded);
    } else {
      searchParams.delete("update-needed");
    }

    let newUrl = $page.url.pathname;
    if (searchParams.toString()) {
      newUrl += `?${searchParams.toString()}`;
    }

    goto(newUrl, { replaceState: true, keepFocus: true, noScroll: true });
  }

  // Status options
  const statusOptions: Choice<ServiceStatus | "">[] = [
    { value: "", label: "Tout" },
    {
      value: "PUBLISHED",
      label: "Publié",
      icon: earthFillIcon,
      selectedLabel: "Status : Publié",
    },
    {
      value: "DRAFT",
      label: "Brouillon",
      icon: draftFillIcon,
      selectedLabel: "Status : Brouillon",
    },
    {
      value: "ARCHIVED",
      label: "Archivé",
      selectedLabel: "Status : Archivé",
      icon: folderFillIcon,
    },
    {
      value: "SUGGESTION",
      label: "Suggestion",
      selectedLabel: "Status : Suggestion",
      icon: fileEditFillIcon,
    },
  ];

  // Update status
  const updateNeededOptions: Choice<"true" | "false" | "">[] = [
    { value: "", label: "Tout" },
    {
      value: "true",
      label: "Actualisation nécessaire",
      selectedLabel: "Actualisation : nécessaire",
      icon: errorWarningIcon,
    },
    {
      value: "false",
      label: "Actualisation non nécessaire",
      selectedLabel: "Actualisation : non nécessaire",
      icon: alertIcon,
    },
  ];

  // Service order
  let selectedOrder = $state("modificationDateDesc");
  const serviceOrderOptions: Choice[] = [
    {
      value: "modificationDateDesc",
      label: "Trier par ordre décroissant",
      selectedLabel: "Tri : Par date d’actualisation",
      icon: arrowUpLineIcon,
      iconOnRight: true,
    },
    {
      value: "modificationDateAsc",
      label: "Trier par ordre croissant",
      selectedLabel: "Tri : Par date d’actualisation",
      icon: arrowDownLineIcon,
      iconOnRight: true,
    },
  ];

  function sortService(services) {
    let sortedServices = services.sort((a, b) => {
      let diff =
        new Date(b.modificationDate).getTime() -
        new Date(a.modificationDate).getTime();

      if (selectedOrder === "modificationDateAsc") {
        diff = -1 * diff;
      }

      // By name if needed
      if (diff === 0) {
        diff = a.name.localeCompare(b.name, "fr", { numeric: true });
      }

      return diff;
    });

    if (limit) {
      sortedServices = sortedServices.slice(0, limit);
    }
    return sortedServices;
  }

  function filterAndSortServices(services) {
    if (serviceStatus) {
      // By status
      if (serviceStatus === "ARCHIVED") {
        services = structure.archivedServices;
      } else {
        services = structure.services.filter(
          (service) => service.status === serviceStatus
        );
      }
    }

    // By update status
    if (updateNeeded) {
      services = services.filter((service) =>
        updateNeeded === "true" ? service.updateNeeded : !service.updateNeeded
      );
    }

    return sortService(services);
  }

  function handleEltChange(event) {
    if (event.detail === "update-needed") {
      updateNeeded = event.value;
    }
    if (event.detail === "status") {
      serviceStatus = event.value;
    }
    servicesDisplayed = filterAndSortServices(structure.services);
    updateUrlQueryParams();
  }

  function handleResetFilters() {
    serviceStatus = undefined;
    updateNeeded = undefined;
    servicesDisplayed = filterAndSortServices(structure.services);
    updateUrlQueryParams();
  }

  run(() => {
    servicesDisplayed = filterAndSortServices(structure.services);
  });

  let servicesToUpdate = $derived(structure.services.filter(
    (service) => service.updateNeeded
  ));
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <div class="gap-s8 flex flex-row">
    <h2 class="mb-s0 text-france-blue">Services</h2>
    {#if limit}<Count>{total}</Count>{/if}
  </div>
  <div class="gap-s16 flex flex-wrap">
    {#if !!servicesDisplayed.length && !tabDisplay}
      <LinkButton
        label="Voir tous les services"
        to="/structures/{structure.slug}/services"
        small
        noBackground
      />
    {/if}
    {#if structure.canEditServices}
      <LinkButton
        label="Ajouter un service"
        icon={addIcon}
        to="/services/creer?structure={structure.slug}"
      />
    {/if}
  </div>
</div>

{#if !hasAtLeastOneServiceNotArchived(structure) && structure.isMember && structure.canEditServices && withEmptyNotice}
  <div class="mb-s24">
    <NoServiceNotice />
  </div>
{/if}

{#if (hasAtLeastOneServiceNotArchived(structure) || hasArchivedServices(structure)) && tabDisplay && structure.canEditServices}
  <div
    class="mb-s40 px-s24 py-s24 text-f14 md:h-s80 md:py-s0 flex w-full flex-wrap items-center rounded-lg bg-white shadow-md"
  >
    <div class="gap-s16 flex w-full flex-wrap items-center">
      <div class="text-f16 flex w-full items-center font-bold md:w-auto">
        Filtrer par&nbsp;:
      </div>

      <div>
        <SelectField
          label="Statut"
          name="status"
          placeholder="Statut"
          value={serviceStatus}
          choices={statusOptions}
          hideLabel
          style="filter"
          minDropdownWidth="min-w-[175px]"
          onChange={handleEltChange}
        />
      </div>
      <div>
        <SelectField
          label="Actualisation"
          name="update-needed"
          placeholder="Actualisation"
          value={updateNeeded}
          choices={updateNeededOptions}
          hideLabel
          style="filter"
          minDropdownWidth="min-w-[265px]"
          onChange={handleEltChange}
        />
      </div>

      <div class="text-right sm:flex-1">
        <button
          class:!text-magenta-cta={serviceStatus || updateNeeded}
          class="text-gray-text-alt"
          onclick={handleResetFilters}
        >
          Tout effacer
        </button>
      </div>
    </div>
  </div>

  <div class="mb-s40 gap-s16 flex flex-col justify-between sm:flex-row">
    <div>
      <strong>
        {servicesDisplayed.length} service{servicesDisplayed.length > 1
          ? "s"
          : ""}
      </strong>
      <span class:hidden={!serviceStatus && !updateNeeded}>
        correspond{servicesDisplayed.length > 1 ? "ent" : ""} à votre recherche
      </span>
    </div>

    <div class="text-f14 inline-block min-w-[280px]">
      <SelectField
        label="Tri"
        name="services-order"
        placeholder="Tri"
        bind:value={selectedOrder}
        choices={serviceOrderOptions}
        hideLabel
        showIconForSelectedOption
        onChange={() => (servicesDisplayed = sortService(servicesDisplayed))}
      />
    </div>
  </div>
{/if}
{#if tabDisplay && structure.canEditServices}
  <div class="mb-s24 gap-s24 flex flex-col">
    <ServicesToUpdateNotice
      structureSlug={structure.slug}
      {servicesToUpdate}
      {onRefresh}
    />
    <ServicesToSyncWithModelNotice
      structureSlug={structure.slug}
      services={structure.services}
      {onRefresh}
    />
  </div>
{/if}

<div class="mb-s48 gap-s16 grid md:grid-cols-2 lg:grid-cols-3">
  {#each servicesDisplayed as service}
    <ServiceCard
      {service}
      {servicesOptions}
      readOnly={!structure.canEditServices}
      {onRefresh}
    />
  {/each}
</div>
