<script context="module">
  import { getStructure, getStructureServices } from "$lib/structures";

  export async function load({ page }) {
    const currentTab = page.path.endsWith("/services") ? 2 : 1;
    return {
      props: {
        structure: await getStructure(page.params.slug),
        services: await getStructureServices(page.params.slug, {
          publishedOnly: true,
        }),
        currentTab,
      },
    };
  }
</script>

<script>
  import { structureStore, servicesStore } from "./_store";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import StructureHeader from "./_structure-header.svelte";

  export let structure, services, currentTab;

  structureStore.set(structure);
  servicesStore.set(services);
</script>

<CenteredGrid --col-bg="var(--col-magenta-brand)" topPadded>
  <div class="col-span-full">
    <StructureHeader {structure} {currentTab} />
  </div>
</CenteredGrid>

<CenteredGrid
  roundedbg
  --col-under-bg="var(--col-magenta-brand)"
  --col-content-bg="var(--col-bg)"
>
  <slot />
</CenteredGrid>
