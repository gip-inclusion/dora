<script context="module">
  import { get } from "svelte/store";
  import { userInfo } from "$lib/auth";
  import { getStructure, getStructureServices } from "$lib/structures";

  export async function load({ params }) {
    const slug = params.slug;
    const structure = await getStructure(slug);
    const info = get(userInfo);
    const canEdit = structure.isMember || info?.isStaff;
    const services = await getStructureServices(slug, {
      publishedOnly: !canEdit,
    });

    return {
      props: {
        structure,
        services,
      },
      stuff: {
        structure,
        services,
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";

  export let structure;
  export let services;
</script>

<CenteredGrid --col-bg="var(--col-magenta-brand)" topPadded>
  <div class="col-span-full">
    <Header {structure} hasServices={!!services?.length} />
  </div>
</CenteredGrid>

<CenteredGrid
  roundedbg
  --col-under-bg="var(--col-magenta-brand)"
  --col-content-bg="var(--col-bg)"
  topPadded
>
  <slot />
</CenteredGrid>
