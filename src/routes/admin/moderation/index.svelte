<script>
  import { onMount } from "svelte";
  import { getStructuresToModerate, getServicesToModerate } from "$lib/admin";

  import { capitalize, shortenString } from "$lib/utils";
  import LinkButton from "$lib/components/link-button.svelte";
  import { eyeIcon } from "$lib/icons";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import ModerationLabel from "../_moderation-label.svelte";
  import { ModerationStatus } from "$lib/enums";
  let services, structures, entities;
  let filteredEntities = [];

  const STATUS_VALUE = {
    [ModerationStatus.NEED_INITIAL_MODERATION]: 1,
    [ModerationStatus.NEED_NEW_MODERATION]: 2,
    [ModerationStatus.IN_PROGRESS]: 3,
    [ModerationStatus.VALIDATED]: 4,
  };
  onMount(async () => {
    structures = await getStructuresToModerate();
    structures.forEach((s) => (s.isStructure = true));
    services = await getServicesToModerate();
    entities = [...structures, ...services];
    filteredEntities = filterAndSortEntities("");
  });

  function filterAndSortEntities(searchString) {
    let result = (
      searchString
        ? entities.filter((s) => {
            if (s.isStructure) {
              return (
                s.name.toLowerCase().includes(searchString) ||
                s.department === searchString
              );
            } else {
              return (
                s.name.toLowerCase().includes(searchString) ||
                s.structureName.toLowerCase().includes(searchString) ||
                s.structureDept === searchString
              );
            }
          })
        : entities
    )
      .filter((s) => !s.parent)
      .sort((s1, s2) => {
        // On tri d'abord par statut de modération
        const val1 = s1.moderationStatus
          ? STATUS_VALUE[s1.moderationStatus]
          : 999;
        const val2 = s2.moderationStatus
          ? STATUS_VALUE[s2.moderationStatus]
          : 999;
        if (val1 !== val2) return val1 - val2;
        // Puis les structures en premier
        if (s1.isStructure && !s2.isStructure) return -1;
        if (s2.isStructure && !s1.isStructure) return 1;
        // Puis par dept de structure
        const sdept1 = s1.isStructure ? s1.department : s1.structureDept;
        const sdept2 = s1.isStructure ? s1.department : s1.structureDept;
        if (sdept1 !== sdept2) return sdept1 > sdept2;
        // Puis par nom de structure
        const sname1 = s1.isStructure ? s1.name : s1.structureName;
        const sname2 = s1.isStructure ? s1.name : s1.structureName;
        if (sname1 !== sname2) return sname1 > sname2;
        // Finalement par nom
        return s1.name > s2.name;
      });
    return result;
  }

  function handleFilterChange(event) {
    const searchString = event.target.value.toLowerCase().trim();
    filteredEntities = filterAndSortEntities(searchString);
  }
</script>

<svelte:head>
  <title>Admin | Structures | DORA</title>
</svelte:head>

<CenteredGrid bgColor="bg-gray-bg">
  <h2>Moderation</h2>

  <div class="flex flex-col gap-s12">
    <div class="mb-s12 flex w-full flex-row items-center gap-s12">
      <div class="grow">
        <input
          on:input={handleFilterChange}
          class="w-full border border-gray-02 p-s8"
          placeholder="rechercher (nom du service, de la structure ou numéro du département)…"
        />
      </div>

      {#if entities && filteredEntities && entities?.length !== filteredEntities?.length}
        <div class="text-gray-text">
          ({filteredEntities.length} / {entities.length})
        </div>
      {/if}
    </div>

    {#if entities}
      {#if !entities.length}
        Rien à modérer 🎉
      {:else}
        {#each filteredEntities as entity}
          <div
            class="flex flex-row items-center gap-s16 rounded-md bg-white p-s16"
          >
            {#if entity.isStructure}
              <div class="grow">
                <a href="/admin/structures/{entity.slug}" target="_blank">
                  <span class="font-bold">
                    🏢 {shortenString(capitalize(entity.name))}
                  </span><br />
                  <span class="text-f12">{entity.department}</span>
                </a>
              </div>

              <ModerationLabel
                status={entity.moderationStatus}
                date={entity.moderationDate}
              />
              <LinkButton
                to="/structures/{entity.slug}"
                icon={eyeIcon}
                noBackground
                otherTab
              />
            {:else}
              <div class="grow ">
                <a href="/admin/services/{entity.slug}" target="_blank">
                  <span class="mb-s0 font-bold">
                    {shortenString(entity.name)}
                  </span><br />
                  <span class="text-f12"
                    >{entity.structureName} ({entity.structureDept})</span
                  >
                </a>
              </div>
              <ModerationLabel
                status={entity.moderationStatus}
                date={entity.moderationDate}
              />
              <div class="flex-none basis-s32">
                <LinkButton
                  to="/services/{entity.slug}"
                  icon={eyeIcon}
                  noBackground
                  otherTab
                />
              </div>
            {/if}
          </div>
        {/each}
      {/if}
    {:else}
      Chargement…
    {/if}
  </div>
</CenteredGrid>
