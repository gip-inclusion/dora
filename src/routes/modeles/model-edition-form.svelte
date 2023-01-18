<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import FormErrors from "$lib/components/display/form-errors.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import FieldsDocuments from "$lib/components/specialized/services/fields-documents.svelte";
  import FieldsModalities from "$lib/components/specialized/services/fields-modalities.svelte";
  import FieldsPeriodicity from "$lib/components/specialized/services/fields-periodicity.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsStructure from "$lib/components/specialized/services/fields-structure.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import { createOrModifyModel } from "$lib/requests/services";
  import type { Model, ServicesOptions, ShortStructure } from "$lib/types";
  import { modelSchema } from "$lib/validation/schemas/service";

  export let model: Model;
  export let servicesOptions: ServicesOptions;
  export let structures: ShortStructure[];
  export let structure: ShortStructure;

  let requesting = false;

  function handleChange(validatedData) {
    structure = { ...model, ...validatedData };
  }

  function handleSubmit(validatedData) {
    return createOrModifyModel(validatedData);
  }

  async function handleSuccess(result) {
    goto(`/modeles/${result.slug}`);
  }
</script>

<FormErrors />

<Form
  data={model}
  schema={modelSchema}
  {servicesOptions}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <hr />
  <CenteredGrid bgColor="bg-gray-bg">
    {#if structures.length}
      <div class="lg:w-2/3">
        <FieldsStructure
          schema={modelSchema}
          bind:structure
          bind:service={model}
          bind:servicesOptions
          {structures}
          isModel
        />
      </div>
    {/if}
  </CenteredGrid>

  <hr />

  <CenteredGrid bgColor="bg-gray-bg">
    <div class="lg:w-2/3">
      {#if model?.structure}
        <FieldsPresentation
          noTopPadding
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />

        <FieldsTypology
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />

        <FieldsPublics
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />

        <FieldsModalities
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />

        <FieldsDocuments
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />

        <FieldsPeriodicity
          bind:service={model}
          {servicesOptions}
          {model}
          schema={modelSchema}
        />
      {/if}
    </div>
  </CenteredGrid>

  <hr />

  {#if model?.structure}
    <CenteredGrid>
      <div class="flex flex-row gap-s12">
        <Button
          name="validate"
          type="submit"
          label="Enregistrer"
          disabled={requesting}
        />
      </div></CenteredGrid
    >
  {/if}
</Form>
