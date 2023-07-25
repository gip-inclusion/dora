<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
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
    searchString: string;
    selectedCategories: ServiceCategory[];
    selectedTypologies: Typology[][number]["value"][];
    sortChoice: SortingChoice;
  }

  const emptySearchParams: SearchParams = {
    searchString: "",
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

  function isOrphan(struct) {
    return !struct.hasAdmin && !struct.adminsToRemind.length;
  }
  function waiting(struct) {
    return struct.adminsToRemind.length;
  }

  function toModerate(struct) {
    return struct.moderationStatus !== "VALIDATED";
  }

  function toActivate(struct) {
    return !struct.numPublishedServices;
  }

  function toUpdate(struct) {
    return struct.numOutdatedServices;
  }

  function filterAndSortEntities(
    structs: AdminShortStructure[],
    params: SearchParams
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
          !params.selectedTypologies.length ||
          params.selectedTypologies.includes(struct.typology)
        );
      })
      .filter((struct) => {
        if (searchStatus === "orphelines") {
          return isOrphan(struct);
        } else if (searchStatus === "en_attente") {
          return !isOrphan(struct) && waiting(struct);
        } else if (searchStatus === "à_modérer") {
          return !isOrphan(struct) && !waiting(struct) && toModerate(struct);
        } else if (searchStatus === "à_activer") {
          return (
            !isOrphan(struct) &&
            !waiting(struct) &&
            !toModerate(struct) &&
            toActivate(struct)
          );
        } else if (searchStatus === "à_actualiser") {
          return (
            !isOrphan(struct) &&
            !waiting(struct) &&
            !toModerate(struct) &&
            !toActivate(struct) &&
            toUpdate(struct)
          );
        } else if (searchStatus === "toutes") {
          return true;
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

  $: filteredStructures = filterAndSortEntities(structures, searchParams);
</script>

<div class="mb-s8 font-bold">Actions en attente :</div>

<div class="mb-s8 flex gap-s8">
  <Button
    on:click={() => {
      resetSearchParams();
      searchStatus = "orphelines";
    }}
    label="orphelines"
    secondary={searchStatus !== "orphelines"}
  />

  <Button
    on:click={() => {
      resetSearchParams();
      searchStatus = "en_attente";
    }}
    label="en attente"
    secondary={searchStatus !== "en_attente"}
  />

  <Button
    on:click={() => {
      resetSearchParams();
      searchStatus = "à_modérer";
    }}
    label="à modérer"
    secondary={searchStatus !== "à_modérer"}
  />

  <Button
    on:click={() => {
      resetSearchParams();
      searchStatus = "à_activer";
    }}
    label="à activer "
    secondary={searchStatus !== "à_activer"}
  />

  <Button
    on:click={() => {
      resetSearchParams();
      searchStatus = "à_actualiser";
    }}
    label="à actualiser"
    secondary={searchStatus !== "à_actualiser"}
  />
</div>

<Button
  on:click={() => {
    resetSearchParams();
    searchStatus = "toutes";
  }}
  label="Afficher toutes les structures"
  noBackground
  small
/>

<div class="mt-s16 flex flex-col gap-s12">
  <div class="mb-s12 flex w-full flex-row items-center gap-s12">
    <div class="grow">
      <label for="filter-by-name-siret">Recherche par nom ou par SIRET</label>
      <input
        id="filter-by-name-siret"
        bind:value={searchParams.searchString}
        class="w-full border border-gray-02 p-s8"
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
    class="mx-s8  rounded border border-gray-01 p-s16"
  >
    <div class="mb-s16 flex flex-col gap-s24">
      <div class="flex justify-between gap-s16">
        <div class="flex grow flex-col">
          <label for="typologies">Typologies</label>
          <Select
            id="typologies"
            multiple
            bind:value={searchParams.selectedTypologies}
            choices={structuresOptions.typologies}
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

      <div class="flex justify-between gap-s16">
        <div class="flex grow flex-col">
          <label for="moderation">Trier par…</label>
          <Select
            id="sort"
            bind:value={searchParams.sortChoice}
            choices={SORTING_CHOICES}
          />
        </div>
      </div>
      <div class="flex justify-between gap-s16" />
    </div>
  </div>
</div>

<style lang="postcss">
  label {
    @apply font-bold;
  }
</style>
