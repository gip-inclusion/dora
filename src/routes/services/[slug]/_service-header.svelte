<script>
  import Label from "$lib/components/label.svelte";

  import Tag from "$lib/components/tag.svelte";
  import { checkBoxBlankIcon, mapPinIcon } from "$lib/icons";

  import StructureCard from "$lib/components/structures/card.svelte";

  export let service;
</script>

<div class="col-span-full col-start-1 py-s32 text-white">
  <div class="mx-auto">
    <div class="flex flex-col gap-s16 lg:flex-row lg:justify-between">
      <div class="lg:w-2/3">
        <div class="flex items-center">
          {#if !service.isDraft && !service.isSuggestion}
            <Label
              label="Disponible"
              icon={checkBoxBlankIcon}
              success
              darkBg
              bold
              smallIcon
            />
            <p class="mx-s12 mb-s0 text-f12 text-gray-03">|</p>
          {/if}

          <p class="mb-s0 text-f12 text-gray-01">
            Mis à jour le {new Date(
              service.modificationDate
            ).toLocaleDateString("fr-FR", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        </div>
        <h1 class="text-white">{service.name}</h1>
        <div class="mb-s16 flex flex-wrap gap-s8">
          {#each service.categoriesDisplay.sort( (a, b) => a.localeCompare( b, "fr", { numeric: true } ) ) as categoryDisplay}
            <Tag
              selfStart
              bgColorClass="bg-magenta-brand"
              textColorClass="text-white">{categoryDisplay}</Tag
            >
          {/each}
        </div>

        <Label
          label={service.diffusionZoneDetailsDisplay}
          icon={mapPinIcon}
          darkBg
        />
      </div>

      <div class="lg:w-1/3 lg:self-end">
        <StructureCard structure={service.structureInfo} />
      </div>
    </div>
  </div>
</div>

<style lang="postcss">
  @media print {
    h1 {
      color: var(--col-france-blue);
    }
  }
</style>
