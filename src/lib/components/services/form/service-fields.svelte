<script>
  import { onDestroy, onMount } from "svelte";
  import { serviceSchema } from "$lib/schemas/service";
  import debounce from "lodash.debounce";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import Button from "$lib/components/button.svelte";
  import Notice from "$lib/components/notice.svelte";

  import FieldsStructure from "./_fields-structure.svelte";
  import FieldsCommon from "./_fields-common.svelte";
  import FieldsService from "./_fields-service.svelte";
  import ServiceNavButtons from "./_service-nav-buttons.svelte";
  import Errors from "./_errors.svelte";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";

  export let service, servicesOptions, structures, structure, model;

  let errorDiv;

  function onError() {
    errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
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

  // Counter for filling duration
  let intervalId;
  let lastUserActivity, userIsInactive;

  // Note: we use debounce to limit update frequency
  const updateLastUserActivity = debounce(() => {
    lastUserActivity = Date.now();
  }, 500);

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
        typologyFieldDisabled={model && model.canUpdateCategory === false}
      />
    </div>
  </CenteredGrid>

  <hr />

  <CenteredGrid bgColor="bg-gray-bg">
    <div class="lg:w-2/3">
      <FieldsService
        bind:service
        {servicesOptions}
        {serviceSchema}
        {structure}
      />
    </div>
  </CenteredGrid>
  <hr />

  <CenteredGrid>
    <div class="flex flex-row gap-s12">
      <ServiceNavButtons {onError} {servicesOptions} bind:service />
    </div>
  </CenteredGrid>
{/if}
