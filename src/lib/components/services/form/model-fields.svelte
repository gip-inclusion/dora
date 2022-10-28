<script>
  import { modelSchema } from "$lib/schemas/service";

  import FieldsCommon from "./_fields-common.svelte";
  import ModelNavButtons from "./_model-nav-buttons.svelte";
  import Errors from "./_errors.svelte";
  import FieldsStructure from "./_fields-structure.svelte";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";

  export let servicesOptions, structures, model, structure;

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }
</script>

<hr />

<CenteredGrid bgColor="bg-gray-bg">
  <div bind:this={errorDiv} />
  <Errors />

  <div class="lg:w-2/3">
    {#if structures.length}
      <FieldsStructure
        bind:structure
        bind:service={model}
        bind:servicesOptions
        {structures}
        serviceSchema={modelSchema}
        isModel
      />
    {/if}

    {#if model?.structure}
      <FieldsCommon
        bind:service={model}
        {servicesOptions}
        isModel
        serviceSchema={modelSchema}
        canAddChoices={!model.customizableChoicesSet}
        typologyFieldDisabled={model && model.canUpdateCategories === false}
      />
    {/if}
  </div>
</CenteredGrid>

{#if model?.structure}
  <hr />
  <CenteredGrid>
    <ModelNavButtons {onError} {servicesOptions} bind:model />
  </CenteredGrid>
{/if}
