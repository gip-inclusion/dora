<script lang="ts">
  import { browser } from "$app/env";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  import { userInfo } from "$lib/auth";
  import SelectField from "$lib/components/form/select/select-field.svelte";

  import LinkButton from "$lib/components/link-button.svelte";
  import ServiceCard from "$lib/components/services/service-card.svelte";
  import {
    addCircleIcon,
    arrowDownLineIcon,
    arrowUpLineIcon,
    earthFillIcon,
    fileEditFillIcon,
    folderFillIcon,
    draftFillIcon,
    alertIcon,
    errorWarningIcon,
  } from "$lib/icons";
  import {
    SERVICE_STATUSES,
    SERVICE_UPDATE_STATUS,
    type Choice,
    type DashboardService,
  } from "$lib/types";
  import { computeUpdateStatusData } from "$lib/utils/service";

  export let structure, total, servicesOptions;
  export let hasOptions = true;
  export let onRefresh;
  export let limit: number | undefined = undefined;

  export let serviceStatus: SERVICE_STATUSES | undefined;
  export let updateStatus: SERVICE_UPDATE_STATUS | undefined;
  export let servicesDisplayed: DashboardService[] = [];

  let canEdit;

  function updateUrlQueryParams() {
    if (!browser) return;

    let searchParams = $page.url.searchParams;

    if (serviceStatus) {
      searchParams.set("service-status", encodeURIComponent(serviceStatus));
    } else {
      searchParams.delete("service-status");
    }

    if (updateStatus) {
      searchParams.set("update-status", encodeURIComponent(updateStatus));
    } else {
      searchParams.delete("update-status");
    }

    let newUrl = $page.url.pathname;
    if (searchParams.toString()) newUrl += `?${searchParams.toString()}`;

    goto(newUrl, { replaceState: true, keepfocus: true, noscroll: true });
  }

  // Status options
  const statusOptions: Choice[] = [
    { value: "", label: "Tout" },
    {
      value: SERVICE_STATUSES.PUBLISHED,
      label: "Publié",
      icon: earthFillIcon,
      selectedLabel: "Status : Publié",
    },
    {
      value: SERVICE_STATUSES.DRAFT,
      label: "Brouillon",
      icon: draftFillIcon,
      selectedLabel: "Status : Brouillon",
    },
    {
      value: SERVICE_STATUSES.ARCHIVED,
      label: "Archivé",
      selectedLabel: "Status : Archivé",
      icon: folderFillIcon,
    },
    {
      value: SERVICE_STATUSES.SUGGESTION,
      label: "Suggestion",
      selectedLabel: "Status : Suggestion",
      icon: fileEditFillIcon,
    },
  ];

  // Update status
  const updateStatusOptions: Choice[] = [
    { value: "", label: "Tout" },
    {
      value: SERVICE_UPDATE_STATUS.NEEDED,
      label: "Actualisation conseillée",
      selectedLabel: "Actualisation : conseillée",
      icon: errorWarningIcon,
    },
    {
      value: SERVICE_UPDATE_STATUS.REQUIRED,
      label: "Actualisation requise",
      selectedLabel: "Actualisation : requise",
      icon: alertIcon,
    },
  ];

  // Service order
  let selectedOrder = "modificationDateDesc";
  let serviceOrderOptions: Choice[] = [
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

  function sortService(se) {
    let sse = se.sort((a, b) => {
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
      sse = sse.slice(0, limit);
    }

    return sse;
  }

  function handleEltChange(event) {
    if (event.detail === "update-status") {
      updateStatus = event.value;
    }
    if (event.detail === "status") {
      serviceStatus = event.value;
    }
    servicesDisplayed = filterAndSortServices(structure.services);
  }

  function filterAndSortServices(services) {
    if (serviceStatus) {
      // By status
      if (serviceStatus === SERVICE_STATUSES.ARCHIVED)
        services = structure.archivedServices;
      else {
        services = structure.services.filter((s) => s.status === serviceStatus);
      }
    }

    // By update status
    if (updateStatus) {
      services = services.filter(
        (s) => computeUpdateStatusData(s).updateStatus === updateStatus
      );
    }

    updateUrlQueryParams();
    return sortService(services);
  }

  $: servicesDisplayed = filterAndSortServices(structure.services);
  $: canEdit = structure.isMember || $userInfo?.isStaff;
</script>

<div class="mb-s24 md:flex md:items-center md:justify-between">
  <h2 class="text-france-blue">Services</h2>
  <div class="flex gap-s16">
    {#if !!servicesDisplayed.length && !hasOptions}
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
        iconOnRight
        icon={addCircleIcon}
        to="/services/creer?structure={structure.slug}"
      />
    {/if}
  </div>
</div>
{#if hasOptions && canEdit}
  <div
    class="mb-s40 flex h-s80 w-full items-center justify-between rounded-md bg-white px-s24 text-f14 shadow-md"
  >
    <div class="flex items-center gap-s16">
      <div class="text-f16 font-bold">Filtrer par&nbsp;:</div>

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
          name="update-status"
          placeholder="Actualisation"
          value={updateStatus}
          choices={updateStatusOptions}
          hideLabel
          style="filter"
          minDropdownWidth="min-w-[265px]"
          onChange={handleEltChange}
        />
      </div>
    </div>

    <div>
      <button
        class:!text-magenta-cta={serviceStatus || updateStatus}
        class="text-gray-text-alt"
        on:click={() => {
          serviceStatus = undefined;
          updateStatus = undefined;
        }}
      >
        Tout effacer
      </button>
    </div>
  </div>

  <div class="mb-s40 flex justify-between gap-s16">
    <span>
      <strong>
        {servicesDisplayed.length} service{servicesDisplayed.length > 1
          ? "s"
          : ""}
      </strong>
      <span class:hidden={!serviceStatus && !updateStatus}>
        correspond{servicesDisplayed.length > 1 ? "ent" : ""} à votre recherche
      </span>
    </span>

    <div class="inline-block min-w-[280px] text-f14">
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

<div class="mb-s48 grid gap-s16 md:grid-cols-2 lg:grid-cols-3">
  {#each servicesDisplayed as service}
    <ServiceCard {service} {servicesOptions} readOnly={!canEdit} {onRefresh} />
  {/each}
</div>
