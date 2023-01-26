<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import { eyeIcon } from "$lib/icons";
  import { getStructuresToModerate } from "$lib/requests/admin";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import { onMount } from "svelte";
  import ModerationLabel from "../moderation-label.svelte";

  // let services,
  let structures, entities;
  let filteredEntities = [];

  const STATUS_VALUE = {
    NEED_INITIAL_MODERATION: 1,
    NEED_NEW_MODERATION: 2,
    IN_PROGRESS: 3,
    VALIDATED: 4,
  };

  function filterAndSortEntities(searchString) {
    const result = (
      searchString
        ? entities.filter((entity) => {
            if (entity.isStructure) {
              return (
                entity.name.toLowerCase().includes(searchString) ||
                entity.department === searchString
              );
            } else {
              return (
                entity.name.toLowerCase().includes(searchString) ||
                entity.structureName.toLowerCase().includes(searchString) ||
                entity.structureDept === searchString
              );
            }
          })
        : entities
    )
      .filter((entity) => !entity.parent)
      .sort((entity1, entity2) => {
        // On tri d'abord par statut de modération
        const val1 = entity1.moderationStatus
          ? STATUS_VALUE[entity1.moderationStatus]
          : 999;
        const val2 = entity2.moderationStatus
          ? STATUS_VALUE[entity2.moderationStatus]
          : 999;
        if (val1 !== val2) {
          return val1 - val2;
        }
        // Puis les structures en premier
        if (entity1.isStructure && !entity2.isStructure) {
          return -1;
        }
        if (entity2.isStructure && !entity1.isStructure) {
          return 1;
        }
        // Puis par dept de structure
        const sdept1 = entity1.isStructure
          ? entity1.department
          : entity1.structureDept;
        const sdept2 = entity1.isStructure
          ? entity1.department
          : entity1.structureDept;
        if (sdept1 !== sdept2) {
          return sdept1 > sdept2;
        }
        // Puis par nom de structure
        const sname1 = entity1.isStructure
          ? entity1.name
          : entity1.structureName;
        const sname2 = entity1.isStructure
          ? entity1.name
          : entity1.structureName;
        if (sname1 !== sname2) {
          return sname1 > sname2;
        }
        // Finalement par nom
        return entity1.name > entity2.name;
      });
    return result;
  }

  function handleFilterChange(event) {
    const searchString = event.target.value.toLowerCase().trim();
    filteredEntities = filterAndSortEntities(searchString);
  }

  onMount(async () => {
    structures = await getStructuresToModerate();
    structures.forEach((struct) => (struct.isStructure = true));
    // On désactive la modération des services pour l'instant
    // services = await getServicesToModerate();
    // entities = [...structures, ...services];
    entities = [...structures];
    filteredEntities = filterAndSortEntities("");
  });
</script>

<CenteredGrid>
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
            class="flex flex-row items-center gap-s16 rounded-md border border-gray-01 bg-white p-s16"
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
