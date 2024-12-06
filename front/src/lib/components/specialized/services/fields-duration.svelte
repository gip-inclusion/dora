<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import type { Service } from "$lib/types";

  export let service: Service;
</script>

<FieldSet title="Durée de la prestation">
  <BasicInputField
    type="number"
    id="durationWeeklyHours"
    description="En nombre d'heures"
    bind:value={service.durationWeeklyHours}
  />

  <BasicInputField
    type="number"
    id="durationWeeks"
    description="En nombre de semaines. Si moins d’une semaine, laisser 1."
    bind:value={service.durationWeeks}
  />
</FieldSet>
