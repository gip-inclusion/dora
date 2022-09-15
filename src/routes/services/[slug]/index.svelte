<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getModel, getService, getServicesOptions } from "$lib/services";
  import { token } from "$lib/auth";

  export async function load({ url, params }) {
    const service = await getService(params.slug);
    // si le service est en brouillon il faut un token pour y accéder
    // on renvoie donc un objet vide côté serveur
    if (!service) {
      if (!browser) {
        return {
          props: {
            service: null,
          },
        };
      }
      if (!get(token)) {
        return {
          status: 302,
          redirect: `/auth/connexion?next=${encodeURIComponent(
            url.pathname + url.search
          )}`,
        };
      }
      return {
        status: 404,
        error: "Page Not Found",
      };
    }

    const model = service.model ? await getModel(service.model) : null;

    return {
      props: {
        service,
        servicesOptions: await getServicesOptions({ model }),
      },
    };
  }
</script>

<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import ServiceHeader from "$lib/components/services/body/service-header.svelte";
  import ServiceToolbar from "$lib/components/services/body/toolbar/service-toolbar.svelte";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { NPS_FORM_ID, SERVICE_CREATION_FORM_ID } from "$lib/const";
  import { isAfter } from "$lib/utils/date";
  import type { Service } from "$lib/types";
  import ServicePresentation from "$lib/components/services/body/presentation/service-presentation.svelte";
  import ServiceKeyInformations from "$lib/components/services/body/service-key-informations.svelte";
  import ServiceShare from "$lib/components/services/body/service-share.svelte";
  import ServiceBeneficiaries from "$lib/components/services/body/service-beneficiaries.svelte";
  import ServiceMobilize from "$lib/components/services/body/service-mobilize.svelte";
  import ServiceMobilisation from "$lib/components/services/body/service-mobilisation.svelte";
  import ServiceContact from "$lib/components/services/body/service-contact.svelte";
  import ServiceLoginNotice from "$lib/components/services/body/service-login-notice.svelte";

  export let service: Service;
  export let servicesOptions;

  $: showContactInfo = $token || service?.isContactInfoPublic;
  let isNoticeOpen = true;

  // Nous ne voulons pas afficher le formulaire sur les services avant cette date
  // afin de ne pas avoir une durée de contribution fausse
  const MIN_DATE_FOR_SERVICE_FEEDBACK_FROM = new Date("2022-07-21");

  onMount(() => {
    if (browser) {
      window.plausible("service", {
        props: {
          service: service.name,
          slug: service.slug,
          structure: service.structureInfo.name,
          departement: service.department,
        },
      });
    }
  });

  onDestroy(() => {
    serviceSubmissionTimeMeter.clear();
  });

  async function handleRefresh() {
    service = await getService(service.slug);
  }
</script>

<svelte:head>
  <title>{service?.name} | {service?.structureInfo?.name} | DORA</title>
  <meta name="description" content={service?.shortDesc} />
</svelte:head>

{#if service}
  <CenteredGrid bgColor="bg-france-blue">
    <ServiceHeader {service} />
  </CenteredGrid>
  <hr />
  <div>
    {#if browser}
      <ServiceToolbar {service} {servicesOptions} onRefresh={handleRefresh} />
    {/if}
  </div>

  <CenteredGrid>
    <div class="service-body">
      <div class="presentation">
        <ServicePresentation {service} {servicesOptions} />
      </div>
      <hr class="separator-1" />
      <div class="beneficiaries">
        <ServiceBeneficiaries {service} />
      </div>
      <hr class="separator-2" />
      <div class="mobilize">
        <ServiceMobilize {service} />
      </div>

      <div class="sidebar flex flex-col gap-y-s24">
        {#if service?.isContactInfoPublic || $token}
          <div
            class="block rounded-lg border border-gray-02 p-s24 px-s32 md:hidden"
          >
            <ServiceContact {service} />
          </div>
        {/if}
        <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
          <ServiceKeyInformations {service} display="sidebar" />
        </div>
        <div class="rounded-lg border border-gray-02 p-s32 pb-s48">
          <ServiceShare {service} />
        </div>
      </div>
    </div>
  </CenteredGrid>

  {#if isNoticeOpen && browser}
    <div
      class="sticky bottom-s0 left-s0 right-s0 w-[100vw] bg-white px-s40 shadow-md"
      class:bg-service-blue-light={!showContactInfo}
    >
      <div
        class="mx-auto flex max-w-6xl items-center justify-end py-s20 sm:py-s28 md:justify-between"
      >
        {#if showContactInfo}
          <div class="hidden md:block">
            <ServiceContact {service} presentation="inline" />
          </div>
          <ServiceMobilisation {service} />
        {:else}
          <ServiceLoginNotice bind:isOpen={isNoticeOpen} />
        {/if}
      </div>
    </div>
  {/if}

  {#if $serviceSubmissionTimeMeter.id && $serviceSubmissionTimeMeter.duration && isAfter(new Date(service.creationDate), MIN_DATE_FOR_SERVICE_FEEDBACK_FROM) && !service.hasAlreadyBeenUnpublished}
    <TallyNpsPopup
      formId={SERVICE_CREATION_FORM_ID}
      timeout={3000}
      hiddenFields={{
        service: $serviceSubmissionTimeMeter.id,
        temps: $serviceSubmissionTimeMeter.duration,
      }}
    />
  {/if}

  <!-- Do not display NPS to the service contributor -->
  {#if !service.canWrite}
    <TallyNpsPopup formId={NPS_FORM_ID} />
  {/if}
{/if}

<style>
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
