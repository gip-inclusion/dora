<script context="module">
  import { getStructure, getStructureServices } from "$lib/structures";

  export async function load({ page }) {
    const structure = await getStructure(page.params.slug);
    const services = await getStructureServices(page.params.slug, {
      publishedOnly: true,
    });
    return {
      props: {
        structure,
      },
      stuff: {
        structure,
        services,
      },
    };
  }
</script>

<script>
  import { page } from "$app/stores";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import StructureHeader from "./_structure-header.svelte";

  export let structure;
  $: currentTab = $page.path.endsWith("/services") ? 2 : 1;
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
