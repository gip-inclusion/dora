<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Fieldset from "$lib/components/display/fieldset.svelte";
  import FormErrors from "$lib/components/display/form-errors.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import Form from "$lib/components/hoc/form.svelte";
  import FieldCategory from "$lib/components/specialized/services/field-category.svelte";
  import FieldsContact from "$lib/components/specialized/services/fields-contact.svelte";
  import FieldsDocuments from "$lib/components/specialized/services/fields-documents.svelte";
  import FieldsInclusionNumerique from "$lib/components/specialized/services/fields-inclusion-numerique.svelte";
  import FieldsModalities from "$lib/components/specialized/services/fields-modalities.svelte";
  import FieldsPerimeter from "$lib/components/specialized/services/fields-perimeter.svelte";
  import FieldsPeriodicity from "$lib/components/specialized/services/fields-periodicity.svelte";
  import FieldsPlace from "$lib/components/specialized/services/fields-place.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsStructure from "$lib/components/specialized/services/fields-structure.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import { createOrModifyService } from "$lib/requests/services";
  import type {
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import {
    draftSchema,
    serviceSchema,
    inclusionNumeriqueSchema,
  } from "$lib/validation/schemas/service";
  import { validate } from "$lib/validation/validation";

  export let service: Service,
    servicesOptions: ServicesOptions,
    structures: ShortStructure[],
    structure: ShortStructure,
    model: Model;

  let requesting = false;

  function handleChange(validatedData) {
    service = { ...service, ...validatedData };
  }

  function handleSubmit(validatedData, kind) {
    if (kind === "publish") {
      service.status = "PUBLISHED";
      service.markSynced = true;

      return createOrModifyService({
        ...validatedData,
        status: "PUBLISHED",
      });
    } else if (kind === "draft") {
      service.status = "DRAFT";
      service.markSynced = true;
      // eslint-disable-next-line no-warning-comments
      // HACK: Empty <Select> are casted to null for now
      // but the server wants an empty string
      // We should fix the <Select> instead
      if (service.category == null) {
        service.category = "";
      }
      return createOrModifyService({
        ...validatedData,
        status: "DRAFT",
      });
    } else {
      console.error(kind);
    }
  }

  function handleSuccess(result) {
    goto(`/services/${result.slug}`);
  }

  function handleValidate(data, kind: "draft" | "publish") {
    let schema = kind === "draft" ? draftSchema : serviceSchema;
    return validate(data, schema, {
      servicesOptions,
      checkRequired: kind === "draft" ? false : true,
    });
  }

  let modelSlugTmp = null;

  async function unsync() {
    modelSlugTmp = service.model;
    service.model = null;
  }

  async function sync() {
    service.model = modelSlugTmp;
    modelSlugTmp = null;
  }

  let subcategories = [];
</script>

<FormErrors />

<Form
  data={service}
  schema={serviceSchema}
  {servicesOptions}
  onChange={handleChange}
  onSubmit={handleSubmit}
  onSuccess={handleSuccess}
  onValidate={handleValidate}
  bind:requesting
>
  <hr />
  <CenteredGrid bgColor="bg-gray-bg">
    {#if structures.length}
      <div class="lg:w-2/3">
        <FieldsStructure
          schema={serviceSchema}
          bind:structure
          bind:service
          bind:servicesOptions
          bind:model
          {structures}
        />
      </div>
    {/if}
  </CenteredGrid>

  {#if service?.structure}
    <hr />

    <CenteredGrid bgColor="bg-gray-bg">
      {#if service.model}
        <div class="lg:flex lg:items-center lg:justify-between">
          <h3>Synchronisé avec un modèle</h3>
          <Button
            label="Détacher du modèle"
            secondary
            small
            on:click={unsync}
          />
        </div>
      {/if}

      {#if modelSlugTmp}
        <div class="mb-s24">
          <Notice title="Le service est détaché du modèle" type="warning">
            <p class="text-f14">
              Après enregistrement, cette action sera définitive.
            </p>
            <div slot="button">
              <Button
                label="Re-synchroniser avec le modèle"
                secondary
                small
                on:click={sync}
              />
            </div>
          </Notice>
        </div>
      {:else if service.modelChanged}
        <div class="my-s24">
          <Notice title="Le modèle a été mis à jour" type="warning">
            <p class="text-f14">
              Vous pouvez voir ici les modifications et les utiliser sur le
              service.
            </p>
          </Notice>
        </div>
      {/if}

      {#if !service.useInclusionNumeriqueScheme}
        <div class={service.model ? "" : "lg:w-2/3"}>
          <FieldsTypology
            noTopPadding
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />

          <FieldsPresentation
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />

          <FieldsPublics
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />

          <FieldsModalities
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />

          <FieldsDocuments
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />

          <FieldsPeriodicity
            bind:service
            {servicesOptions}
            {model}
            schema={serviceSchema}
          />
        </div>
        <div class="lg:w-2/3">
          <FieldsPerimeter
            bind:service
            {servicesOptions}
            schema={serviceSchema}
          />

          <FieldsPlace
            bind:service
            {structure}
            {servicesOptions}
            schema={serviceSchema}
          />

          <FieldsContact bind:service schema={serviceSchema} />
        </div>
      {:else}
        <div class={service.model ? "" : "lg:w-2/3"}>
          <Fieldset noTopPadding>
            <FieldCategory
              bind:service
              bind:subcategories
              {servicesOptions}
              {model}
              schema={inclusionNumeriqueSchema}
            />
          </Fieldset>

          <FieldsInclusionNumerique
            bind:service
            bind:subcategories
            {servicesOptions}
            schema={inclusionNumeriqueSchema}
            {structure}
          />
        </div>
      {/if}
    </CenteredGrid>

    <hr />

    <CenteredGrid>
      <div class="flex flex-row gap-s12">
        <Button
          id="draft"
          type="submit"
          label="Enregistrer en brouillon"
          secondary
          disabled={requesting}
        />

        <Button
          id="publish"
          type="submit"
          label="Publier"
          disabled={requesting}
        />
      </div>
    </CenteredGrid>
  {/if}
</Form>
