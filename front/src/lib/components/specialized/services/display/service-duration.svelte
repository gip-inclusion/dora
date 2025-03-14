<script lang="ts">
  import type { Model, Service } from "$lib/types";

  export let service: Service | Model;

  $: isValid =
    isFinite(service.durationWeeklyHours) &&
    service.durationWeeklyHours > 0 &&
    isFinite(service.durationWeeks) &&
    service.durationWeeks > 0;

  $: totalHours = isValid
    ? service.durationWeeklyHours * service.durationWeeks
    : 0;
</script>

<div>
  {#if !isValid}
    <p>Données non renseignées</p>
  {:else}
    <p>
      {service.durationWeeklyHours} heure(s) sur {service.durationWeeks} semaine(s),
      soit {totalHours} heure(s) au total.
    </p>
  {/if}
</div>

<style lang="postcss">
  @reference "../../../../../app.css";

  p {
    @apply m-s0 text-f16 text-gray-text;
  }
</style>
