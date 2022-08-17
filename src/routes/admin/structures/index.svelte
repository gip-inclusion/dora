<script>
  import { onMount } from "svelte";
  import { getStructuresAdmin } from "$lib/admin";

  import { capitalize, shortenString } from "$lib/utils";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import { eyeIcon, homeIcon } from "$lib/icons";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  let structures, filteredStructures;

  onMount(async () => {
    structures = await getStructuresAdmin();
    filteredStructures = filterAndSortEntities("");
  });

  function filterAndSortEntities(searchString) {
    return (
      searchString
        ? structures.filter(
            (s) =>
              s.name.toLowerCase().includes(searchString) ||
              s.department === searchString
          )
        : structures
    ).sort((s1, s2) =>
      s1.department === s2.department
        ? s1.name.toLowerCase().localeCompare(s2.name.toLowerCase(), "fr")
        : s1.department.localeCompare(s2.department, "fr", {
            numeric: true,
          })
    );
  }

  function handleFilterChange(event) {
    const searchString = event.target.value.toLowerCase().trim();
    filteredStructures = filterAndSortEntities(searchString);
  }
</script>

<svelte:head>
  <title>Admin | Structures | DORA</title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <h2>Structures</h2>

  <div class="flex flex-col gap-s12">
    <div class="mb-s12 flex w-full flex-row items-center gap-s12">
      <div class="grow">
        <input
          on:input={handleFilterChange}
          class="w-full border border-gray-02 p-s8"
          placeholder="rechercher (nom de la structure ou numéro du département)…"
        />
      </div>
      {#if structures?.length !== filteredStructures?.length}
        <div class="text-gray-text">
          ({filteredStructures.length} / {structures.length})
        </div>
      {/if}
    </div>

    {#if structures}
      {#each filteredStructures as structure}
        <div class="flex flex-row gap-s16 rounded-md bg-white p-s16">
          <div class="flex grow flex-row items-center">
            <a href="/admin/structures/{structure.slug}" target="_blank">
              <h5>
                {shortenString(capitalize(structure.name))}
                {#if structure.typologyDisplay}({structure.typologyDisplay}){/if}
              </h5>
            </a>
          </div>
          {#if structure.department}
            <Label
              label={structure.department || " "}
              smallIcon
              icon={homeIcon}
            />
          {/if}

          <LinkButton
            to="/structures/{structure.slug}"
            icon={eyeIcon}
            noBackground
            otherTab
          />
        </div>
      {/each}
    {:else}
      Chargement…
    {/if}
  </div>
</CenteredGrid>
