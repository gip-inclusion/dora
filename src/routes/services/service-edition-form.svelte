<script lang="ts">
  import { goto } from "$app/navigation";
  import Button from "$lib/components/display/button.svelte";
  import CenteredGrid from "$lib/components/display/centered-grid.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import Errors from "$lib/components/specialized/services/errors.svelte";
  import FieldsCommon from "$lib/components/specialized/services/fields-common.svelte";
  import FieldsStructure from "$lib/components/specialized/services/fields-structure.svelte";
  import { createOrModifyService, publishDraft } from "$lib/requests/services";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";
  import type {
    Model,
    Service,
    ServicesOptions,
    ShortStructure,
  } from "$lib/types";
  import { logException } from "$lib/utils/logger";
  import { draftSchema, serviceSchema } from "$lib/validation/schemas/service";
  import { injectAPIErrors, validate } from "$lib/validation/validation";
  import debounce from "lodash.debounce";
  import { onDestroy, onMount } from "svelte";
  import FieldsInclusionNumerique from "./inclusion-numerique-fields.svelte";
  import FieldsService from "./standard-fields.svelte";

  export let service: Service,
    servicesOptions: ServicesOptions,
    structures: ShortStructure[],
    structure: ShortStructure,
    model: Model;

  let modelSlugTmp = null;
  let errorDiv;

  // Counter for filling duration
  let intervalId;
  let lastUserActivity, userIsInactive;

  // Note: we use debounce to limit update frequency
  const updateLastUserActivity = debounce(() => {
    lastUserActivity = Date.now();
  }, 500);

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function unsync() {
    modelSlugTmp = service.model;
    service.model = null;
  }

  async function sync() {
    service.model = modelSlugTmp;
    modelSlugTmp = null;
  }

  onMount(() => {
    lastUserActivity = Date.now();
    serviceSubmissionTimeMeter.clear(); // reset tracking values

    intervalId = setInterval(() => {
      userIsInactive = (Date.now() - lastUserActivity) / 1000 > 120; // 2 minutes
      if (document.hasFocus() && !userIsInactive) {
        serviceSubmissionTimeMeter.incrementDuration();
      }
    }, 1000);
  });

  onDestroy(() => {
    clearInterval(intervalId);
  });

  async function publish() {
    service.status = "PUBLISHED";
    service.markSynced = true;

    // Validate the whole form
    const { validatedData, valid } = validate(service, serviceSchema, {
      servicesOptions: servicesOptions,
    });

    if (valid) {
      try {
        let result = await createOrModifyService({
          ...validatedData,
          durationToAdd: $serviceSubmissionTimeMeter.duration,
        });
        result = await publishDraft(result.data.slug);

        // For feedback modal
        serviceSubmissionTimeMeter.setId(result.slug);

        goto(`/services/${result.slug}`);
      } catch (error) {
        logException(error);
      }
    }
  }

  async function saveDraft() {
    service.status = "DRAFT";
    service.markSynced = true;

    // eslint-disable-next-line no-warning-comments
    // HACK: Empty <Select> are casted to null for now
    // but the server wants an empty string
    // We should fix the <Select> instead
    if (service.category == null) {
      service.category = "";
    }

    const { validatedData, valid } = validate(service, draftSchema, {
      servicesOptions: servicesOptions,
    });

    if (!valid) {
      return;
    }

    // Validation OK, let's send it to the API endpoint
    const result = await createOrModifyService({
      ...validatedData,
      durationToAdd: $serviceSubmissionTimeMeter.duration,
    });

    if (result.ok) {
      serviceSubmissionTimeMeter.clear();

      goto(`/services/${result.data.slug}`);
    } else {
      injectAPIErrors(
        result.error || {
          nonFieldErrors: [
            {
              code: "fetch-error",
              message: "Erreur de connexion au serveur",
            },
          ],
        },
        {}
      );

      if (onError) {
        onError();
      }
    }
  }
</script>

<svelte:window
  on:keydown={updateLastUserActivity}
  on:mousemove={updateLastUserActivity}
  on:touchmove={updateLastUserActivity}
/>

<hr />
<CenteredGrid bgColor="bg-gray-bg">
  <div bind:this={errorDiv} />
  <Errors />

  {#if structures.length}
    <div class="lg:w-2/3">
      <FieldsStructure
        bind:structure
        bind:service
        bind:servicesOptions
        bind:model
        {structures}
        {serviceSchema}
      />
    </div>
  {/if}
</CenteredGrid>

{#if service?.structure}
  <hr />

  <CenteredGrid bgColor={service.model ? "bg-info-light" : "bg-gray-bg"}>
    {#if service.model}
      <div class="lg:flex lg:items-center lg:justify-between">
        <h3>Synchronisé avec un modèle</h3>
        <Button label="Détacher du modèle" secondary small on:click={unsync} />
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

    <div class={service.model ? "" : "lg:w-2/3"}>
      <FieldsCommon
        bind:service
        {servicesOptions}
        {model}
        {serviceSchema}
        canAddChoices={!model?.customizableChoicesSet}
        typologyFieldDisabled={model && model.canUpdateCategories === false}
      />
    </div>
  </CenteredGrid>

  <hr />

  <CenteredGrid bgColor="bg-gray-bg">
    <div class="lg:w-2/3">
      {#if service.useInclusionNumeriqueScheme}
        <FieldsInclusionNumerique
          bind:service
          {servicesOptions}
          {serviceSchema}
          {structure}
        />
      {:else}
        <FieldsService
          bind:service
          {servicesOptions}
          {serviceSchema}
          {structure}
        />
      {/if}
    </div>
  </CenteredGrid>
  <hr />

  <CenteredGrid>
    <div class="flex flex-row gap-s12">
      <Button
        on:click={saveDraft}
        name="save"
        label="Enregistrer en brouillon"
        secondary
      />

      <Button on:click={publish} name="publish" label="Publier" />
    </div>
  </CenteredGrid>
{/if}
