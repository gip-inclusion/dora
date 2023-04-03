<script lang="ts">
  // Source pour l'accessibilité : https://www.w3.org/WAI/ARIA/apg/example-index/combobox/combobox-select-only.html
  import { goto } from "$app/navigation";
  import {
    arrowDownSIcon,
    arrowUpSIcon,
    deleteBinIcon,
    draftFillIcon,
    earthFillIcon,
    fileEditFillIcon,
    folderFillIcon,
  } from "$lib/icons";
  import {
    archiveService,
    convertSuggestionToDraft,
    deleteService,
    getService,
    publishService,
    unarchiveService,
    unPublishService,
  } from "$lib/requests/services";
  import type { Service, ServiceStatus, ShortService } from "$lib/types";
  import { clickOutside } from "$lib/utils/misc";
  import { randomId } from "$lib/utils/random";
  import { getAvailableOptionsForStatus } from "$lib/utils/service";
  import { serviceSchema } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";

  type ServiceStatusPresentation = {
    bgClass: string;
    iconClass: string;
    hoverBgClass: string;
    icon: string;
    label: string;
  };

  export const SERVICE_STATUS_PRESENTATION: Record<
    ServiceStatus,
    ServiceStatusPresentation
  > = {
    SUGGESTION: {
      bgClass: "bg-service-violet",
      iconClass: "text-service-violet-darker",
      hoverBgClass: "bg-service-violet-dark",
      icon: fileEditFillIcon,
      label: "Suggestion",
    },
    DRAFT: {
      bgClass: "bg-service-orange",
      iconClass: "text-service-orange-darker",
      hoverBgClass: "bg-service-orange-dark",
      icon: draftFillIcon,
      label: "Brouillon",
    },
    PUBLISHED: {
      bgClass: "bg-service-green",
      iconClass: "text-service-green-darker",
      hoverBgClass: "bg-service-green-dark",
      icon: earthFillIcon,
      label: "Publié",
    },
    ARCHIVED: {
      bgClass: "bg-service-gray",
      iconClass: "text-gray-darker",
      hoverBgClass: "bg-service-gray-dark",
      icon: folderFillIcon,
      label: "Archivé",
    },
  };

  export let service: Service | ShortService;
  export let servicesOptions;
  export let onRefresh: () => void;
  export let hideLabel = true;
  export let fullWidth = false;

  // *** Accessibilité
  const uuid: string = randomId(); // Pour éviter les conflits d'id si le composant est présent plusieurs fois sur la page
  let isDropdownOpen = false;

  // Gestion de l'outline avec la navigation au clavier
  let selectedOptionIndex: number | null = null;
  let selectedOption: ServiceStatus | "DELETE" | null = null;

  // Actions disponibles
  async function publish() {
    let serviceFull = service;
    // teste si on a le service complet
    // ça n'est pas le cas sur les cards de la page structure par exemple

    if (!Object.prototype.hasOwnProperty.call(service, "fullDesc")) {
      serviceFull = await getService(service.slug);
    }

    const isValid = validate(serviceFull, serviceSchema, {
      noScroll: true,
      showErrors: false,
      servicesOptions: servicesOptions,
    }).valid;

    if (isValid) {
      await publishService(service.slug);
    } else {
      goto(`/services/${service.slug}/editer`);
    }
  }

  function toggleCombobox(forceValue?: boolean) {
    isDropdownOpen = forceValue !== undefined ? forceValue : !isDropdownOpen;
    if (isDropdownOpen) {
      selectedOptionIndex = 0;
      selectedOption = availableOptions[selectedOptionIndex];
    } else {
      selectedOptionIndex = null;
      selectedOption = null;
    }
  }

  async function updateServiceStatus(newStatus: ServiceStatus | "DELETE") {
    if (newStatus === "DRAFT") {
      if (service.status === "SUGGESTION") {
        await convertSuggestionToDraft(service.slug);
      } else if (service.status === "PUBLISHED") {
        await unPublishService(service.slug);
      } else if (service.status === "ARCHIVED") {
        await unarchiveService(service.slug);
      }
    } else if (newStatus === "PUBLISHED") {
      await publish();
    } else if (newStatus === "ARCHIVED") {
      await archiveService(service.slug);
    } else if (newStatus === "DELETE") {
      // eslint-disable-next-line no-alert
      if (confirm(`Supprimer la suggestion ${service.name} ?`)) {
        await deleteService(service.slug);
        goto(`/structures/${service.structure}/`);
      }
    }

    toggleCombobox(false);
    if (onRefresh) {
      await onRefresh();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (["Escape", " ", "Enter", "ArrowDown", "ArrowUp"].includes(event.key)) {
      event.preventDefault();
    }
    if (event.code === "Tab" || event.code === "Escape") {
      toggleCombobox(false);
    }

    if (event.code === "Space") {
      toggleCombobox();
    }

    if (event.code === "Enter") {
      if (!isDropdownOpen) {
        toggleCombobox(true);
      } else {
        if (selectedOption) {
          updateServiceStatus(selectedOption);
        }
      }
    }

    if (event.code === "ArrowDown") {
      selectedOptionIndex = (selectedOptionIndex || 0) + 1;
      selectedOptionIndex = selectedOptionIndex % availableOptions.length;

      selectedOption = availableOptions[selectedOptionIndex];
    }
    if (event.code === "ArrowUp") {
      selectedOptionIndex = (selectedOptionIndex || 0) - 1;
      if (selectedOptionIndex < 0) {
        selectedOptionIndex = availableOptions.length - 1;
      }
      selectedOption = availableOptions[selectedOptionIndex];
    }
  }

  function setAsSelected(
    hoveredStatus: ServiceStatus | "DELETE",
    index: number
  ) {
    selectedOptionIndex = index;
    selectedOption = hoveredStatus;
  }

  // *** Valeurs pour l'affichage
  $: currentStatusPresentation = SERVICE_STATUS_PRESENTATION[service.status];
  $: availableOptions = getAvailableOptionsForStatus(service.status);
</script>

<div
  id="service-state-update"
  class="relative flex cursor-pointer items-center rounded-md font-bold text-gray-dark {currentStatusPresentation.bgClass} hover:{currentStatusPresentation.hoverBgClass}"
  use:clickOutside
  on:click_outside={() => toggleCombobox(false)}
>
  <span id={`button-label-${uuid}`} class="sr-only">
    Modifier le status du service
  </span>

  <div
    aria-controls={`listbox-values-${uuid}`}
    aria-expanded={isDropdownOpen}
    aria-haspopup="listbox"
    aria-labelledby={`button-label-${uuid}`}
    id={`update-listbox-${uuid}`}
    class="cursor:pointer flex items-center px-s20 py-s10"
    role="combobox"
    tabindex="0"
    on:click={() => toggleCombobox()}
    on:keydown={handleKeydown}
  >
    <span class:hidden={hideLabel} class="mr-s10">Statut du service :</span>

    <span
      class="{currentStatusPresentation.iconClass} mr-s8 h-s24 w-s24 fill-current"
    >
      {@html currentStatusPresentation.icon}
    </span>

    <span>{currentStatusPresentation.label}</span>
    <span class="ml-s10 h-s24 w-s24 fill-current text-magenta-cta">
      {#if isDropdownOpen}
        {@html arrowUpSIcon}
      {:else}
        {@html arrowDownSIcon}
      {/if}
    </span>
  </div>

  <div
    class:hidden={!isDropdownOpen}
    class:w-full={fullWidth}
    class="absolute top-s48 right-s0 z-20 min-w-[150px] rounded border border-gray-00 bg-white py-s12 px-s12 shadow-md"
    role="listbox"
    id={`listbox-values-${uuid}`}
    aria-labelledby={`button-label-${uuid}`}
    tabindex="-1"
  >
    {#each availableOptions as option, index (option)}
      {#if option === "DELETE"}
        <div
          class="mb-s10 flex items-center rounded bg-transparent p-s10"
          class:bg-service-red={selectedOption === option}
          on:mouseenter={() => setAsSelected(option, index)}
          role="option"
          on:click={() => updateServiceStatus(option)}
        >
          <span class="mr-s8 h-s24 w-s24 fill-current text-service-red-dark">
            {@html deleteBinIcon}
          </span>
          <span>Supprimer</span>
        </div>
      {:else}
        {@const data = SERVICE_STATUS_PRESENTATION[option]}
        <div
          class="mb-s10 flex items-center rounded p-s10 {selectedOption ===
          option
            ? data.hoverBgClass
            : 'bg-transparent'}"
          role="option"
          id={option}
          on:mouseenter={() => setAsSelected(option, index)}
          on:click={() => updateServiceStatus(option)}
        >
          <span class="{data.iconClass} mr-s8 h-s24 w-s24 fill-current">
            {@html data.icon}
          </span>
          <span>{data.label}</span>
        </div>
      {/if}
    {/each}
  </div>
</div>
