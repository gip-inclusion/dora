<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import RadioButtons from "$lib/components/inputs/radio-buttons.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import type {
    AdminShortStructure,
    ModerationStatus,
    ServiceCategory,
    ServicesOptions,
    StructuresOptions,
    Typology,
  } from "$lib/types";

  export let servicesOptions: ServicesOptions;
  export let structuresOptions: StructuresOptions;
  export let structures: AdminShortStructure[] = [];
  export let filteredStructures: AdminShortStructure[];

  let showAdvancedFilters = false;

  const ADMINISTRATION_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "withAdmin", label: "Administrées" },
    { value: "withoutAdmin", label: "Orphelines" },
  ] as const;
  type AdministrationKind = (typeof ADMINISTRATION_CHOICES)[number]["value"];

  const FRESHNESS_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "uptodate", label: "Tous les services sont actualisés" },
    { value: "toupdate", label: "Certains services doivent être actualisés" },
  ] as const;
  type FreshnessChoice = (typeof FRESHNESS_CHOICES)[number]["value"];

  const NUM_SERVICES_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "withServices", label: "Avec des services publiés" },
    { value: "withoutPublishedServices", label: "Sans services publiés" },
    { value: "withoutServices", label: "Sans services" },
  ] as const;
  type NumServicesChoice = (typeof NUM_SERVICES_CHOICES)[number]["value"];

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

  const MODERATION_FILTER_CHOICES = [
    {
      value: "NEED_INITIAL_MODERATION",
      label: "Première modération nécessaire",
    },
    { value: "NEED_NEW_MODERATION", label: "Nouvelle modération nécessaire" },
    { value: "IN_PROGRESS", label: "En cours" },
    { value: "VALIDATED", label: "Validé" },
  ];

  interface SearchParams {
    administrationKind: AdministrationKind;
    freshnessChoice: FreshnessChoice;
    moderationStatusChoices: ModerationStatus[];
    numServicesChoice: NumServicesChoice;
    searchString: string;
    selectedCategories: ServiceCategory[];
    selectedTypologies: Typology[][number]["value"][];
    showPoleEmploi: boolean;
    sortChoice: SortingChoice;
  }

  // Valeurs des filtres
  let searchParams: SearchParams;

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
    params: SearchParams
  ) {
    const query = normalizeString(params.searchString);
    return structs
      .filter(
        (struct) =>
          !query ||
          normalizeString(struct.name).includes(query) ||
          struct.siret.startsWith(query.replace(/\s/g, ""))
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
          !params.moderationStatusChoices.length ||
          params.moderationStatusChoices.includes(struct.moderationStatus)
        );
      })
      .filter((struct) => {
        return (
          !params.selectedTypologies.length ||
          params.selectedTypologies.includes(struct.typology)
        );
      })
      .filter((struct) => {
        if (params.administrationKind === "withAdmin") {
          return struct.hasAdmin;
        }
        if (params.administrationKind === "withoutAdmin") {
          return !struct.hasAdmin;
        }
        return true;
      })
      .filter((struct) => {
        if (params.freshnessChoice === "uptodate") {
          return struct.numOutdatedServices === 0;
        }
        if (params.freshnessChoice === "toupdate") {
          return struct.numOutdatedServices > 0;
        }
        return true;
      })
      .filter((struct) => {
        if (params.numServicesChoice === "withServices") {
          return struct.numPublishedServices > 0;
        }
        if (params.numServicesChoice === "withoutServices") {
          return struct.numServices === 0;
        }
        if (params.numServicesChoice === "withoutPublishedServices") {
          return struct.numPublishedServices === 0;
        }
        return true;
      })
      .filter((struct) => {
        if (!params.showPoleEmploi) {
          return struct.siret.slice(0, 9) !== "130005481" || struct.hasAdmin;
        }
        return true;
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
    searchParams = {
      administrationKind: "all",
      freshnessChoice: "all",
      moderationStatusChoices: [],
      numServicesChoice: "all",
      searchString: "",
      selectedCategories: [],
      selectedTypologies: [],
      showPoleEmploi: false,
      sortChoice: "name",
    };
  }

  resetSearchParams();

  $: filteredStructures = filterAndSortEntities(structures, searchParams);
</script>

<div class="mb-s8 font-bold">Actions en attente :</div>
<div class="mb-s8 flex gap-s8">
  <Button
    on:click={() => {
      resetSearchParams();

      searchParams.moderationStatusChoices = [
        "NEED_INITIAL_MODERATION",
        "NEED_NEW_MODERATION",
        "IN_PROGRESS",
      ];
    }}
    label="à modérer"
    secondary
  />

  <Button
    on:click={() => {
      resetSearchParams();
      searchParams.freshnessChoice = "toupdate";
      searchParams.sortChoice = "numOutdatedServices";
    }}
    label="à actualiser"
    secondary
  />

  <Button
    disabled
    on:click={() => {
      resetSearchParams();
    }}
    label="suggestions à valider"
    secondary
  />
  <Button
    on:click={() => {
      resetSearchParams();
      searchParams.administrationKind = "withoutAdmin";
    }}
    label="orphelines"
    secondary
  />
</div>

<Button
  on:click={() => {
    resetSearchParams();
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
          <label for="administration">Administration</label>
          <Select
            id="administration"
            bind:value={searchParams.administrationKind}
            choices={ADMINISTRATION_CHOICES}
          />
        </div>
        <div class="flex grow flex-col">
          <label for="freshness">Fraicheur des données</label>
          <Select
            id="freshness"
            bind:value={searchParams.freshnessChoice}
            choices={FRESHNESS_CHOICES}
          />
        </div>
        <div class="flex grow flex-col">
          <label for="num-services">Services</label>
          <Select
            id="num-services"
            bind:value={searchParams.numServicesChoice}
            choices={NUM_SERVICES_CHOICES}
          />
        </div>
      </div>
      <div class="flex justify-between gap-s16">
        <div class="flex grow flex-col">
          <label for="moderation">État de modération</label>
          <Select
            id="moderation"
            bind:value={searchParams.moderationStatusChoices}
            choices={MODERATION_FILTER_CHOICES}
            placeholder="choisir un ou des états…"
            placeholderMulti="choisir un ou des états…"
            multiple
          />
        </div>
        <div class="flex grow flex-col">
          <label for="moderation">Trier par…</label>
          <Select
            id="sort"
            bind:value={searchParams.sortChoice}
            choices={SORTING_CHOICES}
          />
        </div>
      </div>
      <div class="flex justify-between gap-s16">
        <div class="flex grow flex-row gap-s16">
          <label for="moderation">Voir les agences Pôle emploi orphelines</label
          >
          <RadioButtons
            id="show-pole-emploi"
            name="show-pole-emploi"
            bind:group={searchParams.showPoleEmploi}
            choices={[
              { value: true, label: "oui" },
              { value: false, label: "non" },
            ]}
          />
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  label {
    @apply font-bold;
  }
</style>
