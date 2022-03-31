<script context="module">
  import { getStructure } from "$lib/structures";

  import { structure } from "./_store";

  export async function load({ params }) {
    const s = await getStructure(params.slug);

    if (!s) {
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    structure.set(s);

    return {};
  }
</script>

<script>
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Header from "./_header.svelte";
</script>

<CenteredGrid --col-bg="var(--col-magenta-brand)" topPadded>
  <div class="col-span-full">
    <Header structure={$structure} />
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
