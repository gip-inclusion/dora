<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceFeedbackButton from "../../../services/[slug]/service-feedback-button.svelte";
  import ServiceDescription from "./service-description.svelte";
  import ServiceDiIdentification from "./service-di-identification.svelte";
  import ServiceDocuments from "./service-documents.svelte";
  import ServiceKeyInformations from "./service-key-informations/service-key-informations.svelte";
  import ServiceOtherInformations from "./service-other-informations.svelte";
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
  <ServiceKeyInformations {service} {servicesOptions} {onFeedbackButtonClick} />

  <ServiceDescription {service} />

  <ServiceSteps {service} {onTrackMobilisation} />

  <ServiceDocuments {service} />

  <ServiceOtherInformations {service} {servicesOptions} />

  <ServiceDiIdentification {service} />

  {#if onFeedbackButtonClick}
    <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
  {/if}
</div>
