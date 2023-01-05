<script lang="ts">
  import StructureCard from "$lib/components/specialized/structure-card.svelte";
  import Date from "$lib/components/utilities/date.svelte";

  export let model;
</script>

<div class="flex flex-col gap-s16 lg:flex-row-reverse lg:justify-between">
  <div class="lg:w-1/3 lg:self-end">
    <StructureCard structure={model.structureInfo} showAddress={false} />
  </div>

  <div class="lg:w-2/3">
    <div class="flex items-center">
      <p class="mb-s0 text-f14 font-bold text-gray-text">Modèle</p>
      <p class="mx-s12 mb-s0 text-f14 text-gray-03">|</p>
      <p class="mb-s0 text-f14 text-gray-text">
        Mis à jour le <Date date={model.modificationDate} />
      </p>
    </div>
    <h1 class="text-france-blue">{model.name}</h1>

    <p class="mb-s0 text-f14">
      {model.numServices} service{model.numServices > 1 ? "s" : ""} synchronisé{model.numServices >
      1
        ? "s"
        : ""}
    </p>
  </div>
</div>
