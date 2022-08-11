<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getService, getServicesOptions, getModel } from "$lib/services";
  import { token } from "$lib/auth";

  export async function load({ url, params }) {
    const service = await getService(params.slug);
    // si le service est en brouillon il faut un token pour y accéder
    // on renvoit donc un objet vide côté serveur
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
          redirect: `/auth/connexion?next=${encodeURIComponent(url.pathname)}`,
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

<script>
  import { onDestroy, onMount } from "svelte";
  import ServiceHeader from "$lib/components/services/service-header.svelte";
  import ServiceToolbar from "$lib/components/services/service-toolbar.svelte";
  import ServiceBody from "$lib/components/services/service-body.svelte";
  import { serviceSubmissionTimeMeter } from "$lib/stores/service-submission-time-meter";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { NPS_FORM_ID, SERVICE_CREATION_FORM_ID } from "$lib/const";
  import { isAfter } from "$lib/utils/date";

  export let service, servicesOptions;
  // Nous ne voulons pas afficher le formulaire sur les services avant cette date
  // afin de ne pas avoir une durée de contribution fausse
  const MIN_DATE_FOR_SERVICE_FEEDBACK_FROM = new Date("2022-07-21");

  onMount(() => {
    if (browser) {
      plausible("service", {
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
  <CenteredGrid bgColor="bg-gray-bg">
    <ServiceHeader {service} />
  </CenteredGrid>
  <hr />
  <CenteredGrid noPadding>
    <div class="noprint py-s24">
      {#if browser}
        <ServiceToolbar {service} {servicesOptions} onRefresh={handleRefresh} />
      {/if}
    </div>
  </CenteredGrid>

  <CenteredGrid>
    <ServiceBody {service} />
  </CenteredGrid>

  {#if $serviceSubmissionTimeMeter.id && $serviceSubmissionTimeMeter.duration && isAfter(new Date(service.creationDate), MIN_DATE_FOR_SERVICE_FEEDBACK_FROM) && !service.hasAlreadyBeenUnpublished}
    <TallyNpsPopup
      formId={SERVICE_CREATION_FORM_ID}
      timeout="3000"
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
