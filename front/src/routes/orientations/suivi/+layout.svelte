<script lang="ts">
  import type { Snippet } from "svelte";
  import HomeSmile2LineBuildings from "svelte-remix/HomeSmile2LineBuildings.svelte";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Tabs from "$lib/components/display/tabs.svelte";
  import { orientationState } from "./state.svelte.js";
  import type { PageData } from "./$types";

  interface Props {
    children?: Snippet;
    data: PageData;
  }

  let { children, data }: Props = $props();

  const orientationTabs = [
    { id: "received", name: "Orientations reçues" },
    { id: "sent", name: "Orientations envoyées" },
  ];
</script>

<CenteredGrid extraClass="pt-s16" bgColor="bg-blue-information" noPadding>
  <Breadcrumb currentLocation="orientation-export" />
  <h1 class="pt-s48">{data.title}</h1>
  <div class="gap-s8 py-s16 flex">
    <HomeSmile2LineBuildings />
    <a class="underline" href={`/structures/${data.structure.slug}`}
      >{data.structure.typologyDisplay}</a
    >
  </div>
  <Tabs
    items={orientationTabs}
    itemId={orientationState.selectedType}
    onSelectedChange={orientationState.setSelectedType}
  />
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-information">
  {@render children?.()}
</CenteredGrid>
