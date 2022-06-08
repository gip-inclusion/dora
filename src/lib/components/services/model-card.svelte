<script>
  import Label from "$lib/components/label.svelte";
  import ModelMenu from "./model-button-menu.svelte";
  export let model;
  export let readOnly = true;
</script>

<div class="flex flex-col justify-between rounded-md bg-white shadow-md">
  <div
    class="flex grow flex-col justify-between rounded-t-md bg-gray-00 px-s20 py-s12"
    class:rounded-b-md={readOnly}
  >
    <div>
      <div class="mb-s8 flex items-center">
        <p class="mb-s0 text-f12 text-gray-text">
          Mis à jour le {new Date(model.modificationDate).toLocaleDateString(
            "fr-FR",
            {
              year: "numeric",
              month: "long",
              day: "numeric",
            }
          )}
        </p>
      </div>
      <h4 class="mb-s8 text-france-blue">
        <a href="/modeles/{model.slug}">{model.name}</a>
      </h4>
    </div>
    {#if model.diffusionZoneDetailsDisplay}
      <Label label={model.diffusionZoneDetailsDisplay} />
    {/if}
  </div>
  {#if !readOnly}
    <div
      class="flex items-center justify-between border-t border-t-gray-03 p-s20"
    >
      <div class="ml-auto self-end"><ModelMenu {model} /></div>
    </div>
  {/if}
</div>
