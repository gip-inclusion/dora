<script context="module">
  import { browser } from "$app/env";
  import { get } from "svelte/store";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import { getService } from "$lib/services";
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

    return {
      props: {
        service,
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
  import FeedbackModal from "./_feedback-modal.svelte";
  import TallyNpsPopup from "$lib/components/tally-nps-popup.svelte";
  import { NPS_FORM_ID } from "$lib/const";

  export let service;
  let showFeedbackModal = false;
  let feedbackTimeout = undefined;

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

      // Show feedback modal after 15 seconds (if needed)
      if (
        $serviceSubmissionTimeMeter.showFeedbackModal &&
        $serviceSubmissionTimeMeter.id === service.slug
      ) {
        feedbackTimeout = setTimeout(() => (showFeedbackModal = true), 15000);
      }
    }
  });

  onDestroy(() => {
    clearTimeout(feedbackTimeout);
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
        <ServiceToolbar {service} onRefresh={handleRefresh} />
      {/if}
    </div>
  </CenteredGrid>

  <CenteredGrid>
    <ServiceBody {service} />
  </CenteredGrid>

  <FeedbackModal bind:isOpen={showFeedbackModal} {service} />

  <!-- Do not display NPS to the service contributor -->
  {#if !service.canWrite}
    <TallyNpsPopup formId={NPS_FORM_ID} />
  {/if}
{/if}
