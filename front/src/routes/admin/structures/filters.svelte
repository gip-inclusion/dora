<script lang="ts">
  import ArrowDownSLineArrows from "svelte-remix/ArrowDownSLineArrows.svelte";
  import ArrowUpSLineArrows from "svelte-remix/ArrowUpSLineArrows.svelte";

  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import Tooltip from "$lib/components/ui/tooltip.svelte";
  import type {
    AdminStructure,
    ServiceCategory,
    ServicesOptions,
    StructuresOptions,
  } from "$lib/types";

  import { getStructureStatus, getStatusLabel } from "./structures-filters";
  import type { StatusFilter } from "./types";

  interface Props {
    searchStatus: StatusFilter;
    filterDefinition?: string;
    filterActions?: string;
    servicesOptions: ServicesOptions;
    structuresOptions: StructuresOptions;
    structures?: AdminStructure[];
    filteredStructures: AdminStructure[];
  }

  let {
    searchStatus = $bindable(),
    filterDefinition = $bindable(),
    filterActions = $bindable(),
    servicesOptions,
    structuresOptions,
    structures = [],
    filteredStructures = $bindable(),
  }: Props = $props();

  const statusFilterSettings: {
    status: StatusFilter;
    label: string;
    definition: string;
    actions?: string;
  }[] = [
    {
      status: "all",
      label: getStatusLabel("all"),
      definition: "Toutes les structures",
    },
    {
      status: "expiredInvitation",
      label: getStatusLabel("expiredInvitation"),
      definition:
        "Structures où un administrateur a été invité mais supprimé au bout de 120 jours (RGPD) en l’absence de réponse à l’invitation",
      actions: "Identifier un autre administrateur.",
    },
    {
      status: "awaitingModeration",
      label: getStatusLabel("awaitingModeration"),
      definition:
        "Structures nouvelles ou ayant un 1er administrateur, nécessitant une validation de conformité",
      actions:
        "Vérifier la conformité de la structure et si les administrateurs font bien partie de ses effectifs. En cas de doute, contacter l’équipe DORA.",
    },
    {
      status: "awaitingActivation",
      label: getStatusLabel("awaitingActivation"),
      definition:
        "Structures avec un administrateur validé sans services publiés",
      actions:
        "Télécharger la liste des structures à activer, copier-coller les emails des administrateurs pour envoyer un mail groupé les invitant à référencer leurs services sur DORA. Les SIAE sont à exclure car elles n’ont pas vocation à référencer des services supplémentaires.",
    },
    {
      status: "awaitingUpdate",
      label: getStatusLabel("awaitingUpdate"),
      definition:
        "Structures ayant un ou des services publiés qui nécessitent une actualisation",
      actions:
        "Télécharger la liste des structures à activer, copier-coller les emails des administrateurs pour envoyer un mail groupé les invitant à actualiser leur services.",
    },
    {
      status: "obsolete",
      label: "Désactivées",
      definition:
        "Structures désactivées - qui n’existent plus ou qui ne respectent pas la charte DORA",
    },
  ];

  let showAdvancedFilters = $state(false);

  const SORTING_CHOICES = [
    { value: "name", label: "Nom" },
    { value: "numPublishedServices", label: "Nombre de services publiés" },
    {
      value: "numServices",
      label: "Nombre de services (publiés ou en brouillon)",
    },
    { value: "numOutdatedServices", label: "Nombre de services à actualiser" },
  ] as const;
  type SortingChoice = (typeof SORTING_CHOICES)[number]["value"];

  interface SearchParams {
    searchString: string;
    selectedCategories: ServiceCategory[];
    selectedReseauxPorteurs: string[];
    sortChoice: SortingChoice;
  }

  const emptySearchParams: SearchParams = {
    searchString: "",
    selectedCategories: [],
    selectedReseauxPorteurs: [],
    sortChoice: "name",
  };

  let searchParams: SearchParams = $state(emptySearchParams);

  function normalizeString(str: string): string {
    return (
      str
        .trim()
        .toLowerCase()
        // décomposition canonique, les caractères accentués vont être décomposé en
        // caractère ascii + diacritique
        .normalize("NFD")
        // si on voulait supprimer seulement les diacritiques…
        //.replace(/[\u0300-\u036f]/g, '')
        // mais dans le cas présent, on enlève tous les caractères non ascii
        .replace(/([^0-9a-zA-Z])/g, "")
    );
  }

  function filterAndSortEntities(
    structs: AdminStructure[],
    params: SearchParams,
    status: StatusFilter
  ) {
    const query = normalizeString(params.searchString);
    return structs
      .filter(
        (struct) =>
          !query ||
          normalizeString(struct.name).includes(query) ||
          struct.siret?.startsWith(query.replace(/\s/g, ""))
      )
      .filter((struct) => {
        return (
          !params.selectedCategories.length ||
          struct.categories.some((structureCat: ServiceCategory) =>
            params.selectedCategories.includes(structureCat)
          )
        );
      })
      .filter((struct) => {
        return (
          !params.selectedReseauxPorteurs.length ||
          (struct.reseauxPorteurs ?? []).some((reseau) =>
            params.selectedReseauxPorteurs.includes(reseau)
          )
        );
      })
      .filter((struct) => {
        return status === "all" || getStructureStatus(struct) === status;
      })
      .sort((structure1, structure2) => {
        // Fait un premier tri par nom
        return normalizeString(structure1.name).localeCompare(
          normalizeString(structure2.name),
          "fr"
        );
      })
      .sort((structure1, structure2) => {
        // Puis retrie par le critère principal
        switch (params.sortChoice) {
          case "numOutdatedServices":
            return (
              structure2.numOutdatedServices - structure1.numOutdatedServices
            );
          case "numPublishedServices":
            return (
              structure2.numPublishedServices - structure1.numPublishedServices
            );
          case "numServices":
            return structure2.numServices - structure1.numServices;
          default:
            return 0;
        }
      });
  }

  function resetSearchParams() {
    searchParams = emptySearchParams;
    searchStatus = "all";
  }

  // La définition et les actions suivent le filtre courant, y compris quand
  // celui-ci est défini via l'URL.
  $effect(() => {
    const setting = statusFilterSettings.find(
      ({ status }) => status === searchStatus
    );
    filterDefinition = setting?.definition;
    filterActions = setting?.actions;
  });

  $effect(() => {
    filteredStructures = filterAndSortEntities(
      structures,
      searchParams,
      searchStatus
    );
  });
</script>

<h2 class="mb-s12 text-f18 text-gray-dark font-bold">
  Filtrer les {structures.length} structures de mon territoire
</h2>

<div class="mb-s8 gap-s8 flex flex-wrap">
  {#each statusFilterSettings as { status, label, definition }}
    <Tooltip>
      <Button
        onclick={() => {
          resetSearchParams();
          searchStatus = status;
        }}
        label={`${label} (${filterAndSortEntities(structures, searchParams, status).length})`}
        secondary={searchStatus !== status}
        small
      />
      {#snippet content()}
        <div class="max-w-s256 text-center">{definition}</div>
      {/snippet}
    </Tooltip>
  {/each}
</div>

<div class="mt-s16 gap-s12 flex flex-col">
  <div class="mb-s12 gap-s12 flex w-full flex-row items-center">
    <div class="grow">
      <label for="filter-by-name-siret">Recherche par nom ou par SIRET</label>
      <input
        id="filter-by-name-siret"
        bind:value={searchParams.searchString}
        class="border-gray-02 p-s8 w-full border"
        placeholder="Rechercher par nom…"
      />
    </div>
  </div>
</div>

<div class="mb-s32">
  <Button
    label="Voir les filtres avancés"
    onclick={() => (showAdvancedFilters = !showAdvancedFilters)}
    icon={!showAdvancedFilters ? ArrowDownSLineArrows : ArrowUpSLineArrows}
    iconOnRight
    noBackground
    small
  />
  <div
    class:hidden={!showAdvancedFilters}
    class="mx-s8 border-gray-01 p-s16 rounded-sm border"
  >
    <div class="mb-s16 gap-s24 flex flex-col">
      <div class="gap-s16 flex flex-col justify-between md:flex-row">
        <div class="flex grow flex-col">
          <label for="reseaux-porteurs">Réseaux porteurs</label>
          <Select
            id="reseaux-porteurs"
            multiple
            bind:value={searchParams.selectedReseauxPorteurs}
            choices={structuresOptions.reseauxPorteurs ?? []}
            placeholder="Choisir…"
            placeholderMulti="Choisir…"
            sort
          />
        </div>
        <div class="flex grow flex-col">
          <label for="categories">Thématiques</label>
          <Select
            id="categories"
            multiple
            bind:value={searchParams.selectedCategories}
            choices={servicesOptions.categories}
            placeholder="Choisir…"
            placeholderMulti="Choisir…"
            sort
          />
        </div>
      </div>

      <div class="gap-s16 flex justify-between">
        <div class="flex grow flex-col">
          <label for="sort">Trier par…</label>
          <Select
            id="sort"
            bind:value={searchParams.sortChoice}
            choices={SORTING_CHOICES}
          />
        </div>
      </div>
      <div class="gap-s16 flex justify-between"></div>
    </div>
  </div>
</div>

<style lang="postcss">
  @reference "../../../app.css";

  label {
    @apply font-bold;
  }
</style>
