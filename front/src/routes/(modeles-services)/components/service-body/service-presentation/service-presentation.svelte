<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceFeedbackButton from "../../../services/[slug]/service-feedback-button.svelte";
  import ServiceDiIdentification from "./service-di-identification.svelte";
  import ServiceTypology from "./service-typology.svelte";
  import ServiceEligibility from "./service-eligibility.svelte";
  import ServiceConditions from "./service-conditions.svelte";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    onFeedbackButtonClick?: () => void;
    onTrackMobilisation: (url?: string) => void;
  }

  let { service, servicesOptions, onFeedbackButtonClick }: Props = $props();
</script>

<div class="gap-s36 flex flex-col">
  <ServiceTypology {service} {servicesOptions} />

  <ServiceEligibility {service} {servicesOptions} />

  <ServiceConditions {service} />

  <ServiceDiIdentification {service} />

  {#if onFeedbackButtonClick}
    <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
  {/if}
</div>
