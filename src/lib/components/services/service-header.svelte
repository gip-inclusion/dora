<script>
  import Label from "$lib/components/label.svelte";

  import { checkBoxBlankIcon } from "$lib/icons";

  import StructureCard from "$lib/components/structures/card.svelte";

  export let service;
  export let isModel = false;
</script>

<div class="flex flex-col gap-s16 lg:flex-row-reverse lg:justify-between">
  <div class="lg:w-1/3 lg:self-end">
    <StructureCard structure={service.structureInfo} showAddress={false} />
  </div>

  <div class="lg:w-2/3">
    <div class="flex items-center">
      {#if !isModel && !service.isDraft && !service.isSuggestion}
        <Label
          label="Disponible"
          icon={checkBoxBlankIcon}
          success
          bold
          smallIcon
        />
        <p class="mx-s12 mb-s0 text-f12 text-gray-03">|</p>
      {/if}

      <p class="mb-s0 text-f12 text-gray-text">
        Mis à jour le {new Date(service.modificationDate).toLocaleDateString(
          "fr-FR",
          {
            year: "numeric",
            month: "long",
            day: "numeric",
          }
        )}
      </p>
    </div>
    <h1 class="text-france-blue">{service.name}</h1>

    {#if !isModel}
      <Label label={service.diffusionZoneDetailsDisplay} />
    {/if}
  </div>
</div>
