<script context="module">
  import { getStructure } from "$lib/structures";

  export async function load({ params }) {
    const slug = params.slug;
    const structure = await getStructure(slug);

    if (!structure) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    return {
      props: {
        structure,
      },
      stuff: {
        structure,
      },
    };
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";

  export let structure;
</script>

<CenteredGrid --col-bg="var(--col-magenta-brand)" topPadded>
  <div class="col-span-full">
    <Header
      {structure}
      hasServices={!!structure?.services?.length}
      hasBranches={!!structure?.branches?.length}
    />
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
