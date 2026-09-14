<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";

  let {
    servicesOptions,
    service = $bindable(),
    model,
  }: FieldGroupProps = $props();

  let showModel = $derived(!!service.model);

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  let fieldModelProps = $derived(
    model
      ? getModelInputProps({
          service,
          servicesOptions,
          showModel,
          onUseModelValue: handleUseModelValue,
          model,
          schema: $currentSchema,
        })
      : {}
  );
</script>

<FieldGroup title="Publics">
  {#if servicesOptions.publics.length}
    <FieldModel {...fieldModelProps.publics ?? {}} type="array">
      <MultiSelectField
        id="publics"
        bind:value={service.publics}
        choices={servicesOptions.publics}
        sort
        description="Tous publics par défaut. Un ou plusieurs publics possibles. Vous pouvez apporter des précisions sur les publics concernés."
        placeholder="Tous publics"
      />
    </FieldModel>
    <FieldModel {...fieldModelProps.publicsPrecisions}>
      <TextareaField
        id="publicsPrecisions"
        bind:value={service.publicsPrecisions}
        placeholder="Ajoutez ici des précisions sur les publics concernés..."
        hideLabel
      />
    </FieldModel>
  {/if}
</FieldGroup>
