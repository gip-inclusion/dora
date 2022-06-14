<script>
  import Label from "$lib/components/label.svelte";

  import { checkBoxBlankIcon } from "$lib/icons";

  import StructureCard from "$lib/components/structures/card.svelte";
  import Date from "../date.svelte";

  export let service;
</script>

<div class="flex flex-col gap-s16 lg:flex-row-reverse lg:justify-between">
  <div class="lg:w-1/3 lg:self-end">
    <StructureCard structure={service.structureInfo} showAddress={false} />
  </div>

  <div class="lg:w-2/3">
    <div class="flex items-center">
      <p class="mb-s0 text-f14 font-bold text-gray-text">Service</p>
      <p class="mx-s12 mb-s0 text-f14 text-gray-03">|</p>
      {#if !service.isDraft && !service.isSuggestion}
        <Label
          label="Disponible"
          icon={checkBoxBlankIcon}
          success
          bold
          smallIcon
        />
        <p class="mx-s12 mb-s0 text-f14 text-gray-03">|</p>
      {/if}

      <p class="mb-s0 text-f14 text-gray-text">
        Mis à jour le <Date date={service.modificationDate} />
      </p>
    </div>
    <h1 class="text-france-blue">{service.name}</h1>

    <Label label={service.diffusionZoneDetailsDisplay} />
  </div>
</div>
