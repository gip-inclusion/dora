<script lang="ts">
  import type { Service } from "$lib/types";

  export let service: Service;

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
    <p class="">
      {service.durationWeeklyHours} heure(s) sur {service.durationWeeks} semaine(s),
      soit {totalHours} heure(s) au total.
    </p>
  {/if}
</div>

<style lang="postcss">
  p {
    @apply m-s0 text-f16 text-gray-text;
  }
</style>
