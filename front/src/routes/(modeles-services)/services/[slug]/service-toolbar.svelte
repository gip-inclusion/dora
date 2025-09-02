<script lang="ts">
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import type { Service, ServicesOptions } from "$lib/types";

  import ServiceActionButtons from "./service-action-buttons.svelte";
  import ServiceUpdateButtons from "./service-update-buttons.svelte";
  import ServiceUpdateDate from "./service-update-date.svelte";

  interface Props {
    service: Service;
    servicesOptions: ServicesOptions;
    onRefresh: () => void;
    onFeedbackButtonClick: () => void;
  }

  let { service, servicesOptions, onRefresh, onFeedbackButtonClick }: Props =
    $props();
</script>

{#if service.modificationDate}
  <div class="hidden print:block">
    <RelativeDateLabel date={service.modificationDate} prefix="Actualisé le" />
  </div>
{/if}

<div
  class="border-gray-02 py-s40 gap-s24 relative flex flex-col items-center justify-between border-b sm:flex-row print:hidden"
>
  <ServiceUpdateDate {service} {onFeedbackButtonClick} />
  {#if service.canWrite}
    <ServiceUpdateButtons {service} {servicesOptions} {onRefresh} />
  {:else}
    <ServiceActionButtons {service} />
  {/if}
</div>
