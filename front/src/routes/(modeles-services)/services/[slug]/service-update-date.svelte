<script lang="ts">
  import type { Service } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  import ServiceFeedbackButton from "./service-feedback-button.svelte";

  export let service: Service;
  export let onFeedbackButtonClick: () => void;
</script>

<div class="text-f16">
  <div
    class:text-orange={service.updateNeeded}
    class:text-service-green-darker={!service.updateNeeded}
  >
    <RelativeDateLabel
      date={service.modificationDate}
      prefix="Actualisé"
      bold
    />
  </div>
  <ServiceFeedbackButton on:click={onFeedbackButtonClick} />
</div>
