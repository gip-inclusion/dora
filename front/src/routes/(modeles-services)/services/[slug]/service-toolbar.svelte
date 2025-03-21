<script lang="ts">
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";
  import type { Service, ServicesOptions } from "$lib/types";

  import ServiceActionButtons from "./service-action-buttons.svelte";
  import ServiceUpdateButtons from "./service-update-buttons.svelte";
  import ServiceUpdateDate from "./service-update-date.svelte";

  export let service: Service;
  export let servicesOptions: ServicesOptions;
  export let onRefresh: () => void;
</script>

<div class="hidden print:block">
  <RelativeDateLabel date={service.modificationDate} prefix="Actualisé le" />
</div>
<div
  class="border-gray-02 py-s40 gap-s24 relative flex flex-col items-center justify-between border-b sm:flex-row print:hidden"
>
  <ServiceUpdateDate {service} />
  {#if service.canWrite}
    <ServiceUpdateButtons {service} {servicesOptions} {onRefresh} />
  {:else}
    <ServiceActionButtons {service} />
  {/if}
</div>
