<script lang="ts">
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
  } from "$lib/types";
  import { computeUpdateStatusData } from "$lib/utils/service";

  export let structure, total, servicesOptions;
  export let hasOptions = true;
  export let onRefresh;
  export let limit;
  let canEdit;

  // Status options
  let selectedStatus = "";
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
  let selectedUpdateStatus = "";
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
    let services = structure.services;
    if (event.detail === "update-status") {
      selectedUpdateStatus = event.value;
    }
    if (event.detail === "status") {
      selectedStatus = event.value;
    }

    if (selectedStatus) {
      // By status
      if (selectedStatus === SERVICE_STATUSES.ARCHIVED)
        services = structure.archivedServices;
      else {
        services = structure.services.filter(
          (s) => s.status === selectedStatus
        );
      }
    }

    // By update status
    if (selectedUpdateStatus) {
      services = services.filter(
        (s) => computeUpdateStatusData(s).updateStatus === selectedUpdateStatus
      );
    }

    servicesDisplayed = sortService(services);
  }

  let servicesDisplayed = sortService(structure.services);
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
          value={selectedStatus}
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
          value={selectedUpdateStatus}
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
        class:!text-magenta-cta={selectedStatus || selectedUpdateStatus}
        class="text-gray-text-alt"
        on:click={() => {
          selectedStatus = "";
          selectedUpdateStatus = "";
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
      <span class:hidden={!selectedStatus && !selectedUpdateStatus}>
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
