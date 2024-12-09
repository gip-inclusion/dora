<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";

  export let model: Model | undefined = undefined;
  export let servicesOptions: ServicesOptions, service: Service;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: showModel = !!service.model;
  $: fieldModelProps = model
    ? getModelInputProps({
        service,
        servicesOptions,
        showModel,
        onUseModelValue: handleUseModelValue,
        model,
      })
    : {};

  $: totalHours =
    (service.durationWeeklyHours || 0) * (service.durationWeeks || 0);
</script>

<FieldSet title="Durée de la prestation">
  <FieldModel {...fieldModelProps.durationWeeklyHours ?? {}}>
    <BasicInputField
      type="number"
      id="durationWeeklyHours"
      description="En nombre d'heures"
      bind:value={service.durationWeeklyHours}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.durationWeeks ?? {}}>
    <BasicInputField
      type="number"
      id="durationWeeks"
      description="En nombre de semaines. Si moins d’une semaine, laisser 1."
      bind:value={service.durationWeeks}
    />
  </FieldModel>

  <Notice type="warning" showIcon={false} titleLevel="h3">
    <div>
      Ce qui correspond à un volume horaire total de <strong
        >{totalHours}</strong
      >
      heures, réparti sur <strong>{service.durationWeeks || 0}</strong> semaines.
    </div>
  </Notice>
</FieldSet>
