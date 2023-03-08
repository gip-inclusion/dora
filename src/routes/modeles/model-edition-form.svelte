<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import Form from "$lib/components/forms/form.svelte";
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
  import Notice from "$lib/components/display/notice.svelte";

  export let model: Model;
  export let servicesOptions: ServicesOptions;
  export let structures: ShortStructure[];
  export let structure: ShortStructure;

  let requesting = false;

  const showMaxCategoriesNotice = (model.categories.length || 0) > 3;

  function handleChange(validatedData) {
    structure = { ...model, ...validatedData };
  }

  function handleSubmit(validatedData) {
    return createOrModifyModel(validatedData);
  }

  function handleSuccess(result) {
    goto(`/modeles/${result.slug}`);
  }
</script>

<FormErrors />

<Form
  bind:data={model}
  schema={modelSchema}
  {servicesOptions}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  bind:requesting
>
  <hr />
  <CenteredGrid>
    {#if model.slug && showMaxCategoriesNotice}
      <div class="mb-s40">
        <Notice
          type="warning"
          title="Votre modèle comporte plus de 3 thématiques"
        >
          <p class="mb-s0 text-f14">
            Les thématiques permettent de qualifier un service sur Dora et ont
            pour objectif d’identifier les freins spécifiques (et principaux)
            que vous aidez à lever dans le cadre de votre accompagnement.
          </p>
          <p class="mb-s0 text-f14">
            Plus vous êtes précis dans le référencement de votre offre, plus
            vous aidez les personnes accompagnant les publics à identifier le
            bon service ciblé sur leur besoin et plus les demandes d’orientation
            que vous recevez seront qualifiées.
          </p>
        </Notice>
      </div>
    {/if}

    {#if structures.length}
      <div class="lg:w-2/3">
        <FieldsStructure
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

  <CenteredGrid>
    <div class="lg:w-2/3">
      {#if model?.structure}
        <FieldsPresentation
          noTopPadding
          bind:service={model}
          {servicesOptions}
          {model}
        />

        <FieldsTypology bind:service={model} {servicesOptions} {model} />

        <FieldsPublics bind:service={model} {servicesOptions} {model} />

        <FieldsModalities bind:service={model} {servicesOptions} {model} />

        <FieldsDocuments bind:service={model} {servicesOptions} {model} />

        <FieldsPeriodicity bind:service={model} {servicesOptions} {model} />
      {/if}
    </div>
  </CenteredGrid>

  {#if model?.structure}
    <StickyFormSubmissionRow>
      <Button
        name="validate"
        type="submit"
        label="Enregistrer"
        disabled={requesting}
      />
    </StickyFormSubmissionRow>
  {/if}
</Form>
