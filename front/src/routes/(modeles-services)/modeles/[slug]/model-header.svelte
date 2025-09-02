<script lang="ts">
  import HomeSmileLineBuildings from "svelte-remix/HomeSmileLineBuildings.svelte";
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import { capitalize } from "$lib/utils/misc";
  import type { Model } from "$lib/types";

  interface Props {
    model: Model;
  }

  let { model }: Props = $props();
</script>

<div class="text-gray-text">
  <Breadcrumb {model} structure={model.structureInfo} currentLocation="model" />

  <div class="gap-s6 text-f14 mt-s48 flex items-center">
    <HomeSmileLineBuildings size="16" />
    <strong>
      <a href="/structures/{model.structureInfo.slug}" class="underline"
        >{capitalize(model.structureInfo.name)}</a
      >
    </strong>
  </div>

  <h1 class="text-magenta-dark text-f38 leading-s48 mt-s16 mb-s24">
    {model.name}
  </h1>

  <div
    class="bg-blue-information-dark px-s8 py-s2 text-f12 inline-flex items-center rounded-sm font-bold text-white uppercase"
  >
    Modèle&nbsp;•&nbsp;{model.numServices}
    {model.numServices > 1 ? "services synchronisés" : "service synchronisé"}
  </div>
</div>
