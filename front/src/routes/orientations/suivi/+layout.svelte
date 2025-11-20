<script lang="ts">
  import type { Snippet } from "svelte";
  import HomeSmile2LineBuildings from "svelte-remix/HomeSmile2LineBuildings.svelte";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import { orientationState, items } from "./state.svelte.js";

  interface Props {
    children?: Snippet;
  }

  let { children, data }: Props = $props();
</script>

<CenteredGrid bgColor="bg-blue-information" noPadding>
  <Breadcrumb currentLocation="orientation-export" />
  <h1 class="my-0">{data.title}</h1>
  <div class="flex">
    <HomeSmile2LineBuildings></HomeSmile2LineBuildings><a
      class="underline"
      href={`/structures/${data.structure.slug}`}>{data.structure.name}</a
    >
  </div>
  <Tabs
    {items}
    itemId={orientationState.selectedType}
    onSelectedChange={orientationState.setSelectedType}
  />
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-information">
  {@render children?.()}
</CenteredGrid>
