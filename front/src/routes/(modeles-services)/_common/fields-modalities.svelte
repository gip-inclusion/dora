<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  import FieldsModalitiesMobilisation from "./fields-modalities-mobilisation.svelte";
  import FieldsModalitiesPersonnes from "./fields-modalities-personnes.svelte";
  import {
    orderedMobilisableParValues,
    orderedModesMobilisationValues,
  } from "./modalities-order";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
  }

  let { servicesOptions, service = $bindable(), model }: Props = $props();

  function handleUseModelValue(fieldName) {
    service[fieldName] = model ? model[fieldName] : undefined;
    service = { ...service }; // Force le re-rendu
  }

  let showModel = $derived(!!service.model);

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

  $effect(() => {
    fieldModelProps.modesMobilisation?.value.sort((a, b) => {
      return (
        orderedModesMobilisationValues[a] - orderedModesMobilisationValues[b]
      );
    });
  });

  $effect(() => {
    fieldModelProps.modesMobilisation?.serviceValue.sort((a, b) => {
      return (
        orderedModesMobilisationValues[a] - orderedModesMobilisationValues[b]
      );
    });
  });

  $effect(() => {
    fieldModelProps.mobilisablePar?.value.sort((a, b) => {
      return orderedMobilisableParValues[a] - orderedMobilisableParValues[b];
    });
  });

  $effect(() => {
    fieldModelProps.mobilisablePar?.serviceValue.sort((a, b) => {
      return orderedMobilisableParValues[a] - orderedMobilisableParValues[b];
    });
  });
</script>

<FieldSet title="Modalités" {showModel}>
  {#snippet help()}
    <div>
      <p class="text-f14">Modalités pour mobiliser le service.</p>
    </div>
  {/snippet}
  <Notice
    type="warning"
    title="Modalités de mobilisation"
    showIcon={false}
    titleLevel="h3"
  >
    Afin que le service puisse être mobilisable, merci d’indiquer qui peut le
    mobiliser et de choisir au moins une modalité de mobilisation.
  </Notice>

  <div class="lg:gap-s8 flex flex-col">
    {#if $currentSchema && "mobilisablePar" in $currentSchema}
      <FieldModel {...fieldModelProps.mobilisablePar ?? {}} type="array">
        <FieldsModalitiesPersonnes
          id="mobilisablePar"
          {service}
          {servicesOptions}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="lg:gap-s8 flex flex-col">
    {#if $currentSchema && "modesMobilisation" in $currentSchema && "lienMobilisation" in $currentSchema}
      <FieldModel
        {...fieldModelProps.modesMobilisation ?? {}}
        subFields={fieldModelProps.modesMobilisation
          ? {
              "utiliser-lien-mobilisation": [
                {
                  label: $currentSchema.lienMobilisation.label,
                  ...fieldModelProps.lienMobilisation,
                },
              ],
            }
          : undefined}
        type="array"
      >
        <FieldsModalitiesMobilisation
          id="modesMobilisation"
          {service}
          {servicesOptions}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="lg:gap-s8 flex flex-col">
    {#if $currentSchema && "mobilisationPrecisions" in $currentSchema}
      <FieldModel {...fieldModelProps.mobilisationPrecisions ?? {}}>
        <TextareaField
          id="mobilisationPrecisions"
          description="Précisez, si nécessaire, les modalités de mobilisation de l’offre."
          bind:value={service.mobilisationPrecisions}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="gap-s24 flex flex-col">
    <FieldModel
      {...fieldModelProps.feeCondition ?? {}}
      serviceValue={service.feeCondition}
      type="text"
    >
      <RadioButtonsField
        id="feeCondition"
        bind:value={service.feeCondition}
        choices={servicesOptions.feeConditions}
        description="Précisez si le service est gratuit ou payant pour les bénéficiaires."
      />
    </FieldModel>

    {#if isNotFreeService(service.feeCondition)}
      <FieldModel {...fieldModelProps.feeDetails ?? {}}>
        <TextareaField
          id="feeDetails"
          description="Détaillez les frais à la charge des bénéficiaires, y compris leurs montants."
          bind:value={service.feeDetails}
        />
      </FieldModel>
    {/if}
  </div>
</FieldSet>
