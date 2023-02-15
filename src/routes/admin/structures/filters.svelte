<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import Select from "$lib/components/inputs/select/select.svelte";
  import { arrowDownSIcon, arrowUpSIcon } from "$lib/icons";
  import type {
    AdminShortStructure,
    ModerationStatus,
    ServiceCategory,
    ServicesOptions,
    StructuresOptions,
  } from "$lib/types";

  export let servicesOptions: ServicesOptions;
  export let structuresOptions: StructuresOptions;
  export let structures: AdminShortStructure[] = [];
  export let filteredStructures: AdminShortStructure[] = [];

  let showAdvancedFilters = false;
  let searchString = "";
  let selectedCategories: ServiceCategory[] = [];
  let selectedTypologies: string[] = [];

  const ADMINISTRATION_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "withAdmin", label: "Administrées" },
    { value: "withoutAdmin", label: "Orphelines" },
  ] as const;
  let administrationKind: (typeof ADMINISTRATION_CHOICES)[number]["value"] =
    "all";

  const FRESHNESS_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "uptodate", label: "À jour" },
    { value: "toupdate", label: "Avec des services à mettre à jour" },
  ] as const;
  let freshnessChoice: (typeof FRESHNESS_CHOICES)[number]["value"] = "all";

  const NUM_SERVICES_CHOICES = [
    { value: "all", label: "Toutes" },
    { value: "withServices", label: "Avec des services publiés" },
    { value: "withoutServices", label: "Sans services publiés" },
  ] as const;
  let numServicesChoice: (typeof NUM_SERVICES_CHOICES)[number]["value"] = "all";

  const MODERATION_FILTER_CHOICES = [
    {
      value: "NEED_INITIAL_MODERATION",
      label: "Première modération nécessaire",
    },
    { value: "NEED_NEW_MODERATION", label: "Nouvelle modération nécessaire" },
    { value: "IN_PROGRESS", label: "En cours" },
    { value: "VALIDATED", label: "Validé" },
  ];
  let moderationStatusChoices: ModerationStatus[] = [];

  function filterAndSortEntities(
    structs: AdminShortStructure[],
    query: string,
    categories = [],
    typologies = [],
    adminKind = "all",
    freshChoice = "all",
    numServChoice = "all",
    modChoices = []
  ) {
    return structs
      .filter((struct) => !query || struct.name.toLowerCase().includes(query))
      .filter((struct) => {
        return (
          !categories.length ||
          struct.categories.some((structureCat: ServiceCategory) =>
            categories.includes(structureCat)
          )
        );
      })
      .filter((struct) => {
        return (
          !modChoices.length || modChoices.includes(struct.moderationStatus)
        );
      })
      .filter((struct) => {
        return !typologies.length || typologies.includes(struct.typology);
      })
      .filter((struct) => {
        if (adminKind === "withAdmin") {
          return struct.hasAdmin;
        }
        if (adminKind === "withoutAdmin") {
          return !struct.hasAdmin;
        }
        return true;
      })
      .filter((struct) => {
        if (freshChoice === "uptodate") {
          return struct.numOutdatedServices === 0;
        }
        if (freshChoice === "toupdate") {
          return struct.numOutdatedServices > 0;
        }
        return true;
      })
      .filter((struct) => {
        if (numServChoice === "withServices") {
          return struct.numPublishedServices > 0;
        }
        if (numServChoice === "withoutServices") {
          return struct.numPublishedServices === 0;
        }
        return true;
      })
      .sort((structure1, structure2) =>
        structure1.department === structure2.department
          ? structure1.name
              .toLowerCase()
              .localeCompare(structure2.name.toLowerCase(), "fr")
          : structure1.department.localeCompare(structure2.department, "fr", {
              numeric: true,
            })
      );
  }

  function handleFilterChange(event) {
    searchString = event.target.value.toLowerCase().trim();
  }

  function resetFilters() {
    administrationKind = "all";
    freshnessChoice = "all";
    numServicesChoice = "all";
    searchString = "";
    selectedCategories = [];
    selectedTypologies = [];
    moderationStatusChoices = [];
  }

  $: filteredStructures = filterAndSortEntities(
    structures,
    searchString,
    selectedCategories,
    selectedTypologies,
    administrationKind,
    freshnessChoice,
    numServicesChoice,
    moderationStatusChoices
  );
</script>

<div class="mb-s8 font-bold">Afficher les structures :</div>
<div class="mb-s8 flex gap-s8">
  <Button
    on:click={() => {
      resetFilters();
    }}
    label="toutes"
    secondary
    small
  />
  <Button
    on:click={() => {
      resetFilters();
      administrationKind = "withoutAdmin";
    }}
    label="orphelines"
    secondary
    small
  />
  <Button
    on:click={() => {
      resetFilters();
      freshnessChoice = "toupdate";
    }}
    label="nécessitant une mise à jour"
    secondary
    small
  />
  <Button
    on:click={() => {
      resetFilters();

      moderationStatusChoices = [
        "NEED_INITIAL_MODERATION",
        "NEED_NEW_MODERATION",
        "IN_PROGRESS",
      ];
    }}
    label="à modérer"
    secondary
    small
  />

  <Button
    disabled
    on:click={() => {
      resetFilters();
    }}
    label="ayant reçu des suggestions"
    secondary
    small
  />
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
            bind:value={selectedTypologies}
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
            bind:value={selectedCategories}
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
            bind:value={administrationKind}
            choices={ADMINISTRATION_CHOICES}
          />
        </div>
        <div class="flex grow flex-col">
          <label for="freshness">Fraicheur</label>
          <Select
            id="freshness"
            bind:value={freshnessChoice}
            choices={FRESHNESS_CHOICES}
          />
        </div>
        <div class="flex grow flex-col">
          <label for="num-services">Services</label>
          <Select
            id="num-services"
            bind:value={numServicesChoice}
            choices={NUM_SERVICES_CHOICES}
          />
        </div>
      </div>
      <div class="flex justify-between gap-s16">
        <div class="flex grow flex-col">
          <label for="moderation">État de modération</label>
          <Select
            id="moderation"
            bind:value={moderationStatusChoices}
            choices={MODERATION_FILTER_CHOICES}
            placeholder="choisir un ou des états…"
            placeholderMulti="choisir un ou des états…"
            multiple
          />
        </div>
      </div>
    </div>

    <div class="flex flex-col gap-s12">
      <div class="mb-s12 flex w-full flex-row items-center gap-s12">
        <div class="grow">
          <input
            bind:value={searchString}
            on:input={handleFilterChange}
            class="w-full border border-gray-02 p-s8"
            placeholder="Rechercher par nom…"
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
