<script lang="ts">
  import { browser } from "$app/environment";
  import { token } from "$lib/auth";
  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import ServicePresentation from "$lib/components/services/body/presentation/service-presentation.svelte";
  import ServiceBeneficiaries from "$lib/components/services/body/service-beneficiaries.svelte";
  import ServiceHeader from "$lib/components/services/body/service-header.svelte";
  import ServiceKeyInformations from "$lib/components/services/body/service-key-informations.svelte";
  import ServiceMobilisation from "$lib/components/services/body/service-mobilisation.svelte";
  import ServiceMobilize from "$lib/components/services/body/service-mobilize.svelte";
  import ServiceShare from "$lib/components/services/body/service-share.svelte";
  import ServiceToolbar from "$lib/components/services/body/toolbar/service-toolbar.svelte";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { getService } from "$lib/services";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";
  import { isAfter } from "$lib/utils/date";
  import { canDisplayNpsForm, TallyFormId } from "$lib/utils/nps";
  import { trackService } from "$lib/utils/plausible";
  import { onDestroy, onMount } from "svelte";
  import type { PageData } from "./$types";

  export let data: PageData;

  // Nous ne voulons pas afficher le formulaire sur les services avant cette date
  // afin de ne pas avoir une durée de contribution fausse
  const MIN_DATE_FOR_SERVICE_FEEDBACK_FROM = new Date("2022-07-21");

  onMount(() => {
    trackService(data.service);
  });

  onDestroy(() => {
    serviceSubmissionTimeMeter.clear();
  });

  async function handleRefresh() {
    data.service = await getService(data.service.slug);
  }

  $: showContact = data.service?.isContactInfoPublic || $token;
  $: structureHasPublishedServices = data.structure?.services.filter(
    (s) => s.status === "PUBLISHED"
  ).length;
</script>

<svelte:head>
  <title
    >{data.service?.name} | {data.service?.structureInfo?.name} | DORA</title
  >
  <meta name="description" content={data.service?.shortDesc} />
</svelte:head>

{#if data.service}
  <CenteredGrid bgColor="bg-france-blue">
    <ServiceHeader service={data.service} />
  </CenteredGrid>
  <hr />
  <div>
    <ServiceToolbar
      service={data.service}
      servicesOptions={data.servicesOptions}
      onRefresh={handleRefresh}
    />
  </div>

  <CenteredGrid>
    <div class="service-body">
      <div class="presentation">
        <ServicePresentation
          service={data.service}
          servicesOptions={data.servicesOptions}
        />
      </div>
      <hr class="separator-1" />
      <div class="beneficiaries">
        <ServiceBeneficiaries service={data.service} />
      </div>
      <hr class="separator-2" />
      <div class="mobilize">
        <ServiceMobilize service={data.service} />
      </div>

      <div class="sidebar flex flex-col gap-y-s24">
        <div
          class="block rounded-lg border border-gray-02 p-s24 px-s32"
          class:print:hidden={!showContact}
        >
          <ServiceMobilisation service={data.service} {showContact} />
        </div>
        <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
          <ServiceKeyInformations
            service={data.service}
            servicesOptions={data.servicesOptions}
            display="sidebar"
          />
        </div>
        <div class="rounded-lg border border-gray-02 p-s32 pb-s48 print:hidden">
          <ServiceShare service={data.service} />
        </div>
      </div>
    </div>
  </CenteredGrid>
  {#if browser}
    {#if data.service.canWrite}
      {#if canDisplayNpsForm(TallyFormId.SERVICE_CREATION_FORM_ID) && $serviceSubmissionTimeMeter.id && $serviceSubmissionTimeMeter.duration && isAfter(new Date(data.service.creationDate), MIN_DATE_FOR_SERVICE_FEEDBACK_FROM) && !data.service.hasAlreadyBeenUnpublished}
        <TallyNpsPopup
          formId={TallyFormId.SERVICE_CREATION_FORM_ID}
          timeout={3000}
          hiddenFields={{
            service: $serviceSubmissionTimeMeter.id,
            temps: $serviceSubmissionTimeMeter.duration,
          }}
        />
      {:else if structureHasPublishedServices}
        <TallyNpsPopup
          formId={TallyFormId.NPS_OFFEROR_FORM_ID}
          timeout={30000}
        />
      {/if}
    {:else}
      <TallyNpsPopup formId={TallyFormId.NPS_SEEKER_FORM_ID} />
    {/if}
  {/if}
{/if}

<style lang="postcss">
  .presentation {
    grid-area: presentation;
  }

  .beneficiaries {
    grid-area: beneficiaries;
  }

  .mobilize {
    grid-area: mobilize;
  }

  .sidebar {
    grid-area: sidebar;
  }

  .service-body {
    display: grid;
    grid-template-columns: 1fr;
    column-gap: 6rem;
    row-gap: 2rem;
    grid-template-areas:
      "presentation"
      "sidebar"
      "separator-1"
      "beneficiaries"
      "separator-2"
      "mobilize";
  }

  @screen md {
    .service-body {
      grid-template-columns: 1fr 300px;
      column-gap: 4rem;
      grid-template-areas:
        "presentation sidebar"
        "separator-1 sidebar"
        "beneficiaries sidebar"
        "separator-2 sidebar"
        "mobilize sidebar";
    }
  }
  @screen lg {
    .service-body {
      grid-template-columns: 1fr 375px;
    }
  }
</style>
