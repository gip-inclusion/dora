<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import {
    isOrphan,
    isObsolete,
    toActivate,
    toModerate,
    toUpdate,
    waiting,
  } from "./structures-filters";
  import type {
    AdminShortStructure,
    ServiceCategory,
    ServicesOptions,
    StructuresOptions,
    Typology,
  } from "$lib/types";
  import type { StatusFilter } from "./types";

  export let searchStatus: StatusFilter;
  export let servicesOptions: ServicesOptions;
  export let structuresOptions: StructuresOptions;
  export let structures: AdminShortStructure[] = [];
  export let filteredStructures: AdminShortStructure[];

  const filterButtons: { status: StatusFilter; label: string }[] = [
    { status: "toutes", label: "Toutes" },
    { status: "orphelines", label: "Sans utilisateur" },
    { status: "en_attente", label: "Administrateur invité" },
    { status: "à_modérer", label: "À valider" },
    { status: "à_activer", label: "Sans service" },
    { status: "à_actualiser", label: "Services à actualiser" },
    { status: "obsolète", label: "Non conforme" },
  ];

  let showAdvancedFilters = false;

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
    nationalLabels: string[];
    searchString: string;
    selectedCategories: ServiceCategory[];
    selectedTypologies: Typology[][number]["value"][];
    sortChoice: SortingChoice;
  }

  const emptySearchParams: SearchParams = {
    searchString: "",
    nationalLabels: [],
    selectedCategories: [],
    selectedTypologies: [],
    sortChoice: "name",
  };

  let searchParams: SearchParams = emptySearchParams;

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
    structs: AdminShortStructure[],
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
          !params.nationalLabels.length ||
          struct.nationalLabels.some((label: string) =>
            params.nationalLabels.includes(label)
          )
        );
      })
      .filter((struct) => {
        return (
          !params.selectedTypologies.length ||
          params.selectedTypologies.includes(struct.typology)
        );
      })
      .filter((struct) => {
        if (status === "obsolète") {
          return isObsolete(struct);
        } else if (status === "orphelines") {
          return !isObsolete(struct) && isOrphan(struct);
        } else if (status === "en_attente") {
          return !isObsolete(struct) && !isOrphan(struct) && waiting(struct);
        } else if (status === "à_modérer") {
          return (
            !isObsolete(struct) &&
            !isOrphan(struct) &&
            !waiting(struct) &&
            toModerate(struct)
          );
        } else if (status === "à_activer") {
          return (
            !isObsolete(struct) &&
            !isOrphan(struct) &&
            !waiting(struct) &&
            !toModerate(struct) &&
            toActivate(struct)
          );
        } else if (status === "à_actualiser") {
          return (
            !isObsolete(struct) &&
            !isOrphan(struct) &&
            !waiting(struct) &&
            !toModerate(struct) &&
            !toActivate(struct) &&
            toUpdate(struct)
          );
        } else if (status === "toutes") {
          // exclusion des structures obsolètes de l'affichage complet
          return !isObsolete(struct);
        }
        console.error("Statut de recherche inconnu");
        return false;
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
    searchStatus = "toutes";
  }

  $: filteredStructures = filterAndSortEntities(
    structures,
    searchParams,
    searchStatus
  );
</script>

<div class="mb-s8 font-bold">Structures nécessitant une action&#8239;:</div>

<div class="mb-s8 gap-s8 flex">
  {#each filterButtons as { status, label }}
    <Button
      on:click={() => {
        resetSearchParams();
        searchStatus = status;
      }}
      label="{label}{status !== 'toutes'
        ? ` (${filterAndSortEntities(structures, searchParams, status).length})`
        : ''}"
      secondary={searchStatus !== status}
    />
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
    on:click={() => (showAdvancedFilters = !showAdvancedFilters)}
    icon={!showAdvancedFilters ? arrowDownSIcon : arrowUpSIcon}
    iconOnRight
    noBackground
    small
  />
  <div
    class:hidden={!showAdvancedFilters}
    class="mx-s8 border-gray-01 p-s16 rounded-sm border"
  >
    <div class="mb-s16 gap-s24 flex flex-col">
      <div class="gap-s16 flex justify-between">
        <div class="flex grow flex-col">
          <label for="typologies">Typologies</label>
          <Select
            id="typologies"
            multiple
            bind:value={searchParams.selectedTypologies}
            choices={structuresOptions.typologies}
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

      <div class="flex grow flex-col">
        <label for="moderation">Labels nationaux…</label>
        <Select
          id="sort"
          multiple
          bind:value={searchParams.nationalLabels}
          choices={structuresOptions.nationalLabels}
        />
      </div>

      <div class="gap-s16 flex justify-between">
        <div class="flex grow flex-col">
          <label for="moderation">Trier par…</label>
          <Select
            id="sort"
            bind:value={searchParams.sortChoice}
            choices={SORTING_CHOICES}
          />
        </div>
      </div>
      <div class="gap-s16 flex justify-between" />
    </div>
  </div>
</div>

<style lang="postcss">
  @reference "../../../app.css";

  label {
    @apply font-bold;
  }
</style>
