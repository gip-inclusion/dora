<script lang="ts">
  import AddCircleLineSystem from "svelte-remix/AddCircleLineSystem.svelte";
  import CheckLineSystem from "svelte-remix/CheckLineSystem.svelte";
  import HomeSmile2LineBuildings from "svelte-remix/HomeSmile2LineBuildings.svelte";
  import SearchLineSystem from "svelte-remix/SearchLineSystem.svelte";

  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import type { ShortStructure } from "$lib/types";

  interface Props {
    structures?: ShortStructure[];
    lastVisitedStructure?: ShortStructure;
    mobileDesign?: boolean;
  }

  let {
    structures = [],
    lastVisitedStructure,
    mobileDesign = false,
  }: Props = $props();

  let filterText = $state("");
  let structuresToDisplay = $derived(
    filterText
      ? structures.filter((struct) =>
          struct.name
            .toLocaleLowerCase()
            .includes(filterText.toLocaleLowerCase())
        )
      : structures
  );
</script>

<div>
  {#if structures.length !== 0}
    <div class="flex w-full items-center lg:w-auto">
      <DropdownMenu
        labelText="Mes structures"
        hideLabel
        withBorders
        {mobileDesign}
      >
        {#snippet label()}
          <div class="flex w-full items-center">
            <span
              class="mr-s8 h-s24 w-s24 text-magenta-cta inline-block fill-current"
            >
              <HomeSmile2LineBuildings />
            </span>
            {#if lastVisitedStructure}
              <a
                class="text-gray-text block w-[150px] overflow-hidden text-ellipsis whitespace-nowrap"
                onclick={(evt) => evt.stopPropagation()}
                href={`/structures/${lastVisitedStructure.slug}`}
              >
                {lastVisitedStructure.name}
              </a>
            {:else}
              <span class="text-gray-text">Vos structures</span>
            {/if}
          </div>
        {/snippet}

        {#if structures.length > 10}
          <div class="mt-s10 relative w-full">
            <label for="structure-filter" class="sr-only">Rechercher</label>
            <input
              id="structure-filter"
              type="text"
              placeholder="Rechercher"
              bind:value={filterText}
              class="left-s0 right-s0 border-gray-03 p-s10 absolute border"
            />
            <span
              class="right-s8 h-s24 w-s24 text-gray-03 absolute top-[11px] z-40 inline-block fill-current"
            >
              <SearchLineSystem />
            </span>
          </div>
        {/if}
        <div class:mt-s56={structures.length > 10}>
          <ul class="p-s2 max-h-[300px] overflow-y-auto">
            {#each structuresToDisplay as structure}
              {@const selected = structure.slug === lastVisitedStructure?.slug}
              <li>
                <a
                  href={`/structures/${structure.slug}`}
                  class="p-s12 text-gray-text hover:bg-magenta-10 flex items-center justify-between whitespace-nowrap"
                  class:text-magenta-cta={selected}
                >
                  {structure.name}

                  {#if selected}
                    <span
                      class="mr-s8 h-s24 w-s24 text-magenta-cta inline-block fill-current"
                    >
                      <CheckLineSystem />
                    </span>
                  {/if}
                </a>
              </li>
            {/each}
          </ul>
        </div>

        {#snippet bottom()}
          <div>
            <a
              class="text-gray-text flex whitespace-nowrap"
              href="/auth/rattachement"
            >
              <span class="mr-s10 h-s24 w-s24 fill-current">
                <AddCircleLineSystem />
              </span>
              <span>Adhérer à une autre structure </span>
            </a>
          </div>
        {/snippet}
      </DropdownMenu>
    </div>
  {/if}
</div>
