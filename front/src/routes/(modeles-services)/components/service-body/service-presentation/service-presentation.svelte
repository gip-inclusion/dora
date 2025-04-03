<script lang="ts">
  import type { Model, Service, ServicesOptions } from "$lib/types";

  import ServiceFeedbackButton from "../../../services/[slug]/service-feedback-button.svelte";
  import ServiceDescription from "./service-description.svelte";
  import ServiceDiIdentification from "./service-di-identification.svelte";
  import ServiceDocuments from "./service-documents.svelte";
  import ServiceKeyInformations from "./service-key-informations/service-key-informations.svelte";
  import ServiceOtherInformations from "./service-other-informations.svelte";
  import ServiceSteps from "./service-steps.svelte";

  export let service: Service | Model;
  export let servicesOptions: ServicesOptions;
  export let onFeedbackButtonClick: () => void;
</script>

<div class="gap-s36 flex flex-col">
  <ServiceKeyInformations {service} {servicesOptions} {onFeedbackButtonClick} />

  <ServiceDescription {service} />

  <ServiceSteps {service} />

  <ServiceDocuments {service} />

  <ServiceOtherInformations {service} {servicesOptions} />

  <ServiceDiIdentification {service} />

  <ServiceFeedbackButton {service} on:click={onFeedbackButtonClick} />
</div>
