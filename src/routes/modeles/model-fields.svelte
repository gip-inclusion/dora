<script lang="ts">
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import { modelSchema } from "$lib/validation/schemas/service";
  import Errors from "$lib/components/specialized/services/errors.svelte";
  import FieldsCommon from "$lib/components/specialized/services/fields-common.svelte";
  import FieldsStructure from "$lib/components/specialized/services/fields-structure.svelte";
  import ModelNavButtons from "./model-nav-buttons.svelte";

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
