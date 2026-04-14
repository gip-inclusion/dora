<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import EyeLineSystem from "svelte-remix/EyeLineSystem.svelte";
  import { capitalize, shortenString } from "$lib/utils/misc";
  import ModerationLabel from "../moderation-label.svelte";
  import { filterAndSortStructures } from "$lib/utils/moderation";

  let { data } = $props();

  let entities = $state([]);
  let searchString = $state("");
  let filteredEntities = $derived(
    filterAndSortStructures(entities, searchString)
  );

  data.structures.then((structures) => {
    entities = [...structures];
  });

  function handleFilterChange(event) {
    searchString = event.target.value.toLowerCase().trim();
  }
</script>

<CenteredGrid>
  <h2>Moderation</h2>

  <div class="gap-s12 flex flex-col">
    <div class="mb-s12 gap-s12 flex w-full flex-row items-center">
      <div class="grow">
        <input
          oninput={handleFilterChange}
          class="border-gray-02 p-s8 w-full border"
          placeholder="rechercher (nom du service, de la structure ou numéro du département)…"
        />
      </div>

      {#if entities && filteredEntities && entities?.length !== filteredEntities?.length}
        <div class="text-gray-text">
          ({filteredEntities.length} / {entities.length})
        </div>
      {/if}
    </div>

    {#await data.structures}
      Chargement…
    {:then _}
      {#if !entities.length}
        Rien à modérer 🎉
      {:else}
        {#each filteredEntities as entity}
          <div
            class="gap-s16 border-gray-01 p-s16 flex flex-row items-center rounded-lg border bg-white"
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
                icon={EyeLineSystem}
                noBackground
                otherTab
              />
            {:else}
              <div class="grow">
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
              <div class="basis-s32 flex-none">
                <LinkButton
                  to="/services/{entity.slug}"
                  icon={EyeLineSystem}
                  noBackground
                  otherTab
                />
              </div>
            {/if}
          </div>
        {/each}
      {/if}
    {/await}
  </div>
</CenteredGrid>
