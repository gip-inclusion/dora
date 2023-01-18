<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import type { Model } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "./field-model.svelte";

  export let servicesOptions, schema, service;
  export let model: Model | undefined = undefined;

  $: showModel = !!service.model;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: fieldModelProps = model
    ? getModelInputProps({
        schema: schema,
        service,
        servicesOptions,
        showModel,
        onUseModelValue: handleUseModelValue,
        model,
      })
    : {};
</script>

<FieldSet title="Périodicité" {showModel}>
  <div slot="help">
    <p class="text-f14">
      La durée limitée permet de supendre automatiquement la visibilité du
      service dans les résultat de recherche.
    </p>
  </div>
  <FieldModel {...fieldModelProps["recurrence"]}>
    <BasicInputField
      id="recurrence"
      schema={schema.recurrence}
      placeholder="Ex. Tous les jours à 14h, une fois par mois, etc."
      bind:value={service.recurrence}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps["suspensionDate"]}>
    <BasicInputField
      id="suspensionDate"
      schema={schema.suspensionDate}
      type="date"
      bind:value={service.suspensionDate}
    />
  </FieldModel>
</FieldSet>
