<script lang="ts">
  import type { Model, Service } from "$lib/types";
  import { isDurationValid } from "$lib/utils/service";
  export let service: Service | Model;

  $: isValid = isDurationValid(service);

  $: totalHours = isValid
    ? service.durationWeeklyHours * service.durationWeeks
    : 0;
</script>

<div>
  {#if !isValid}
    <p class="m-s0 text-f16 text-gray-text">Données non renseignées</p>
  {:else}
    <p class="m-s0 text-f16 text-gray-text">
      {service.durationWeeklyHours} heure(s) sur {service.durationWeeks} semaine(s),
      soit {totalHours} heure(s) au total
    </p>
  {/if}
</div>
