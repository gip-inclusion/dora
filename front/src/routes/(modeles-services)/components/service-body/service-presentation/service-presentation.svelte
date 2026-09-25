<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceFeedbackButton from "../../../services/[slug]/service-feedback-button.svelte";
  import ServiceDiIdentification from "./service-di-identification.svelte";
  import ServiceTypology from "./service-typology.svelte";
  import ServiceDocuments from "./service-documents.svelte";
  import ServiceKeyInformations from "./service-key-informations/service-key-informations.svelte";
  import ServiceSteps from "./service-steps.svelte";

  interface Props {
    service: Service | Model;
    servicesOptions: ServicesOptions;
    onFeedbackButtonClick?: () => void;
    onTrackMobilisation: (url?: string) => void;
  }

  let {
    service,
    servicesOptions,
    onFeedbackButtonClick,
    onTrackMobilisation,
  }: Props = $props();
</script>

<div class="gap-s36 flex flex-col">
  <ServiceTypology {service} {servicesOptions} />

  <ServiceKeyInformations {service} {servicesOptions} {onFeedbackButtonClick} />

  <ServiceSteps {service} {onTrackMobilisation} />

  <ServiceDocuments {service} />

  <ServiceDiIdentification {service} />

  {#if onFeedbackButtonClick}
    <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
  {/if}
</div>
