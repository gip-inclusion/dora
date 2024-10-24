<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import type { Service } from "$lib/types";

  export let service: Service;
</script>

<FieldSet title="Participation du bénéficiaire">
  <BasicInputField
    type="number"
    id="spendingTimeTotalHours"
    description="Nombre total d'heures investies par le bénéficiaire, ex : 18"
    bind:value={service.spendingTimeTotalHours}
  />

  <BasicInputField
    type="text"
    id="spendingTimePrecision"
    description="Précision sur la répartition des heures passées, ex : « 6h par semaine, pendant 3 semaines »"
    bind:value={service.spendingTimePrecision}
  />
</FieldSet>
