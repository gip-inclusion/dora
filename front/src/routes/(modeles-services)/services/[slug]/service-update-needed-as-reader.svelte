<script lang="ts">
  import type { Service } from "$lib/types";
  import RelativeDateLabel from "$lib/components/display/relative-date-label.svelte";

  export let service: Service;
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
  <div class="text-gray-text underline">
    Signalez-nous toute erreur ou suggestion de modification.
  </div>
</div>
