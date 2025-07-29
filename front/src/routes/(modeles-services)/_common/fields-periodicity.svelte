<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
  }

  let { servicesOptions, service = $bindable(), model }: Props = $props();

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

<FieldSet title="Périodicité" {showModel}>
  {#snippet help()}
    <div>
      <p class="text-f14">
        La durée limitée permet de supendre automatiquement la visibilité du
        service dans les résultat de recherche.
      </p>
    </div>
  {/snippet}
  <FieldModel {...fieldModelProps.recurrence ?? {}}>
    <BasicInputField
      id="recurrence"
      descriptionText="Par exemple : tous les jours à 14h, une fois par mois, etc."
      bind:value={service.recurrence}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.suspensionDate ?? {}}>
    <BasicInputField
      id="suspensionDate"
      type="date"
      bind:value={service.suspensionDate}
      descriptionText="Date à partir de laquelle le service ne sera plus visible dans la recherche."
    />
  </FieldModel>

  <FieldModel
    {...fieldModelProps.updateFrequency ?? {}}
    serviceValue={service.updateFrequency}
    type="text"
  >
    <RadioButtonsField
      id="updateFrequency"
      bind:value={service.updateFrequency}
      choices={servicesOptions.updateFrequencies}
      description="À quelle fréquence les informations de votre service changent-elles (description, critères, public, contact) ? Choisissez la période pour être alerté."
    />
  </FieldModel>
</FieldSet>
