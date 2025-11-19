<script lang="ts">
  import type { Snippet } from "svelte";
  import HomeSmile2LineBuildings from "svelte-remix/HomeSmile2LineBuildings.svelte";

  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { getCurrentlySelectedStructure } from "$lib/utils/current-structure";
  import { userInfo } from "$lib/utils/auth";
  import { userPreferences } from "$lib/utils/preferences";
  import Tabs from "$lib/components/display/tabs.svelte";
  import { orientationState } from "./state.svelte.js";

  interface Props {
    children?: Snippet;
  }

  const structure = getCurrentlySelectedStructure($userInfo, $userPreferences);

  let { children }: Props = $props();
</script>

<CenteredGrid bgColor="bg-blue-information" noPadding>
  <Breadcrumb currentLocation="orientation-export" />
  <h1 class="my-0">Suivi des orientations</h1>
  <div class="flex">
    <HomeSmile2LineBuildings></HomeSmile2LineBuildings><a
      class="underline"
      href={`/structures/${structure?.slug}`}>{structure?.name}</a
    >
  </div>
  <Tabs
    items={orientationState.items}
    itemId={orientationState.selectedType}
    onSelectedChange={orientationState.setSelectedType}
  />
</CenteredGrid>

<CenteredGrid roundedColor="bg-blue-information">
  {@render children?.()}
</CenteredGrid>
