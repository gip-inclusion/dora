<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import FormErrors from "$lib/components/forms/form-errors.svelte";
  import StickyFormSubmissionRow from "$lib/components/forms/sticky-form-submission-row.svelte";
  import Form from "$lib/components/forms/form.svelte";
  import FieldsDuration from "$lib/components/specialized/services/fields-duration.svelte";
  import FieldsPresentation from "$lib/components/specialized/services/fields-presentation.svelte";
  import FieldsPublics from "$lib/components/specialized/services/fields-publics.svelte";
  import FieldsTypology from "$lib/components/specialized/services/fields-typology.svelte";
  import FieldsDocuments from "../_common/fields-documents.svelte";
  import FieldsModalities from "../_common/fields-modalities.svelte";
  import FieldsPeriodicity from "../_common/fields-periodicity.svelte";
  import FieldsStructure from "../_common/fields-structure.svelte";
  import { createOrModifyModel } from "$lib/requests/services";
  import type { Model, ServicesOptions, ShortStructure } from "$lib/types";
  import { modelSchema } from "$lib/validation/schemas/service";
  import Notice from "$lib/components/display/notice.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";
  import { showNotice } from "$lib/utils/service-update-notices";

  export let model: Model;
  export let servicesOptions: ServicesOptions;
  export let structures: ShortStructure[];
  export let structure: ShortStructure;
  export let showUpdateAllServicesModal = false;
  let shouldUpdateAllServices = false;

  let requesting = false;
  let submitFormInput;

  const showMaxCategoriesNotice = (model.categories.length || 0) > 3;

  function handleChange(validatedData) {
    structure = { ...model, ...validatedData };
  }
  function handleSubmit(validatedData) {
    showUpdateAllServicesModal = false;
    showNotice("modelSync", structure.slug);
    return createOrModifyModel(validatedData, shouldUpdateAllServices);
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
  <div id="modal-container" />

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
        <FieldsTypology
          noTopPadding
          bind:service={model}
          {servicesOptions}
          {model}
        />

        <FieldsPresentation bind:service={model} {servicesOptions} {model} />

        <FieldsDuration bind:service={model} {servicesOptions} {model} />

        <FieldsPublics bind:service={model} {servicesOptions} {model} />

        <FieldsModalities bind:service={model} {servicesOptions} {model} />

        <FieldsDocuments bind:service={model} {servicesOptions} {model} />

        <FieldsPeriodicity bind:service={model} {servicesOptions} {model} />
      {/if}
    </div>

    {#if shouldUpdateAllServices}
      <Modal
        targetId="modal-container"
        bind:isOpen={showUpdateAllServicesModal}
        title="Mise à jour automatiquement"
        on:close={() => (showUpdateAllServicesModal = false)}
        width="small"
      >
        <div class="pt-s16 text-f14 text-gray-text">
          Vous avez choisi de mettre à jour automatiquement tous les services
          utilisant ce modèle. Si vous aviez ajouté du contenu spécifique dans
          l’un de ces services, il sera remplacé par les nouvelles informations
          du modèle (excepté les informations sur la zone d’éligibilité, le lieu
          de déroulement ou les coordonnées du référent spécifique au service).

          <strong class="mt-s16 block">
            Si ce n’est pas ce que vous souhaitez, cliquez sur annuler, et
            décochez la case.
          </strong>
        </div>

        <div slot="footer">
          <div
            class="mt-s24 gap-s24 flex flex-col-reverse justify-end md:flex-row"
          >
            <Button
              label="Annuler"
              secondary
              on:click={() => (showUpdateAllServicesModal = false)}
            />

            <Button
              id="validate"
              type="submit"
              extraClass="justify-center"
              label="Confirmer"
            />
          </div>
        </div>
      </Modal>
    {/if}
  </CenteredGrid>

  {#if model?.structure}
    <StickyFormSubmissionRow>
      <div class="flex w-full justify-between">
        <div class="flex items-center">
          {#if model.slug}
            <label class="text-f14 text-gray-text flex">
              <input
                type="checkbox"
                bind:checked={shouldUpdateAllServices}
                class="mr-s8"
              />
              Cochez cette case pour mettre à jour automatiquement tous les services
              utilisant ce modèle.
            </label>
          {/if}
        </div>

        {#if shouldUpdateAllServices}
          <Button
            on:click={() => (showUpdateAllServicesModal = true)}
            name="validate"
            type="button"
            label="Enregistrer"
          />
          <input
            bind:this={submitFormInput}
            class="hidden"
            type="submit"
            value="Valider le formulaire"
          />
        {:else}
          <Button
            name="validate"
            type="submit"
            label="Enregistrer"
            disabled={requesting}
          />
        {/if}
      </div>
    </StickyFormSubmissionRow>
  {/if}
</Form>
