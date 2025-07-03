<script lang="ts">
  import DropdownMenu from "$lib/components/display/dropdown-menu.svelte";

  import type { ShortStructure } from "$lib/types";
  import {
    addCircleLineIcon,
    checkIcon,
    homeSmile2Icon,
    searchIcon,
  } from "$lib/icons";

  interface Props {
    structures?: ShortStructure[];
    lastVisitedStructure?: ShortStructure | undefined;
    mobileDesign?: boolean;
  }

  let { structures = [], lastVisitedStructure = undefined, mobileDesign = false }: Props = $props();

  let filterText = $state("");
  let structuresToDisplay = $derived(filterText
    ? structures.filter((struct) =>
        struct.name.toLocaleLowerCase().includes(filterText.toLocaleLowerCase())
      )
    : structures);
</script>

<div class="mb-s16 lg:mb-s0 lg:mr-s10">
  {#if structures.length !== 0}
    <div class="flex w-full items-center lg:w-auto">
      <DropdownMenu label="Mes structures" hideLabel {mobileDesign}>
        <!-- @migration-task: migrate this slot by hand, `label` would shadow a prop on the parent component -->
  <div slot="label" class="flex w-full items-center">
          <span
            class="mr-s8 h-s24 w-s24 text-magenta-cta inline-block fill-current"
          >
            {@html homeSmile2Icon}
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
              {@html searchIcon}
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
                      {@html checkIcon}
                    </span>
                  {/if}
                </a>
              </li>
            {/each}
          </ul>
        </div>

        {#snippet bottom()}
                <div >
            <a
              class="text-gray-text flex whitespace-nowrap"
              href="/auth/rattachement"
            >
              <span class="mr-s10 h-s24 w-s24 fill-current">
                {@html addCircleLineIcon}
              </span>
              <span>Adhérer à une autre structure </span>
            </a>
          </div>
              {/snippet}
      </DropdownMenu>
    </div>
  {/if}
</div>
