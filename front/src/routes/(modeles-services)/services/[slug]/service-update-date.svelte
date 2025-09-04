<script lang="ts">
  import type { Service } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  import ServiceFeedbackButton from "./service-feedback-button.svelte";

  interface Props {
    service: Service;
    onFeedbackButtonClick: () => void;
  }

  let { service, onFeedbackButtonClick }: Props = $props();
</script>

<div class="text-f16">
  <div
    class:text-orange={service.updateNeeded}
    class:text-service-green-darker={!service.updateNeeded}
  >
    {#if service.modificationDate}
      <RelativeDateLabel
        date={service.modificationDate}
        prefix="Actualisé"
        bold
      />
    {/if}
  </div>
  <ServiceFeedbackButton onclick={onFeedbackButtonClick} />
</div>
