<script lang="ts">
  import Breadcrumb from "$lib/components/display/breadcrumb.svelte";
  import { copyIcon2Fill } from "$lib/icons";
  import { capitalize } from "$lib/utils/misc";

  export let model;
</script>

<div
  id="service-header"
  class="gap-s16 relative lg:flex-row-reverse lg:justify-between"
>
  <div class="mb-s48 print:mb-s0">
    <Breadcrumb
      {model}
      structure={model.structureInfo}
      currentLocation="model"
      dark
    />
  </div>

  <div
    class="mb-s28 bg-france-blue px-s12 py-s8 text-f14 inline-flex items-center rounded-lg text-white"
  >
    <span class="mr-s8 h-s16 w-s16 inline-block fill-current text-white">
      {@html copyIcon2Fill}
    </span>
    Modèle&nbsp;•&nbsp;{model.numServices}
    {model.numServices > 1 ? "services synchronisés" : "service synchronisé"}
  </div>

  <div>
    <h1 class="mb-s12 mr-s12 text-france-blue">
      {model.name}
    </h1>
    <p class="text-f23 text-france-blue font-bold">
      {capitalize(model.structureInfo.name)}
    </p>
  </div>
</div>
