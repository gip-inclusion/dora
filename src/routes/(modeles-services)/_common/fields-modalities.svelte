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

  import FieldsModalitiesBeneficiary from "./fields-modalities-beneficiary.svelte";
  import FieldsModalitiesCoach from "./fields-modalities-coach.svelte";
  import {
    orderedBeneficiariesAccessModeValues,
    orderedCoachOrientationModeValues,
  } from "./modalities-order";

  export let servicesOptions: ServicesOptions, service: Service;
  export let model: Model | undefined = undefined;

  function handleUseModelValue(fieldName) {
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

  $: fieldModelProps.coachOrientationModes?.value.sort((a, b) => {
    return (
      orderedCoachOrientationModeValues[a] -
      orderedCoachOrientationModeValues[b]
    );
  });
  $: fieldModelProps.coachOrientationModes?.serviceValue.sort((a, b) => {
    return (
      orderedCoachOrientationModeValues[a] -
      orderedCoachOrientationModeValues[b]
    );
  });
  $: fieldModelProps.beneficiariesAccessModes?.value.sort((a, b) => {
    return (
      orderedBeneficiariesAccessModeValues[a] -
      orderedBeneficiariesAccessModeValues[b]
    );
  });
  $: fieldModelProps.beneficiariesAccessModes?.serviceValue.sort((a, b) => {
    return (
      orderedBeneficiariesAccessModeValues[a] -
      orderedBeneficiariesAccessModeValues[b]
    );
  });
</script>

<FieldSet title="Modalités" {showModel}>
  <div slot="help">
    <p class="text-f14">Modalités pour mobiliser le service.</p>
  </div>
  <Notice
    type="warning"
    title="Modalités d’orientation"
    showIcon={false}
    titleLevel="h3"
  >
    Afin que le service puisse être mobilisable, merci de choisir au moins une
    méthode d’orientation – soit pour l’accompagnateur, soit pour le
    bénéficiaire.
  </Notice>

  <div class="flex flex-col lg:gap-s8">
    {#if $currentSchema && "coachOrientationModes" in $currentSchema && "coachOrientationModesExternalFormLink" in $currentSchema && "coachOrientationModesExternalFormLinkText" in $currentSchema && "coachOrientationModesOther" in $currentSchema}
      <FieldModel
        {...fieldModelProps.coachOrientationModes ?? {}}
        subFields={fieldModelProps.coachOrientationModes
          ? {
              "completer-le-formulaire-dadhesion": [
                {
                  label:
                    $currentSchema.coachOrientationModesExternalFormLink.label,
                  ...fieldModelProps.coachOrientationModesExternalFormLink,
                },
                {
                  label:
                    $currentSchema.coachOrientationModesExternalFormLinkText
                      .label,
                  ...fieldModelProps.coachOrientationModesExternalFormLinkText,
                },
              ],
              autre: [fieldModelProps.coachOrientationModesOther],
            }
          : undefined}
        type="array"
      >
        <FieldsModalitiesCoach
          id="coachOrientationModes"
          {service}
          {servicesOptions}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="flex flex-col lg:gap-s8">
    {#if $currentSchema && "beneficiariesAccessModes" in $currentSchema && "beneficiariesAccessModesExternalFormLink" in $currentSchema && "beneficiariesAccessModesExternalFormLinkText" in $currentSchema && "beneficiariesAccessModesOther" in $currentSchema}
      <FieldModel
        {...fieldModelProps.beneficiariesAccessModes ?? {}}
        subFields={fieldModelProps.beneficiariesAccessModes
          ? {
              "completer-le-formulaire-dadhesion": [
                {
                  label:
                    $currentSchema.beneficiariesAccessModesExternalFormLink
                      .label,
                  ...fieldModelProps.beneficiariesAccessModesExternalFormLink,
                },
                {
                  label:
                    $currentSchema.beneficiariesAccessModesExternalFormLinkText
                      .label,
                  ...fieldModelProps.beneficiariesAccessModesExternalFormLinkText,
                },
              ],
              autre: [fieldModelProps.beneficiariesAccessModesOther],
            }
          : undefined}
        type="array"
      >
        <FieldsModalitiesBeneficiary
          id="beneficiariesAccessModes"
          {service}
          {servicesOptions}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="flex flex-col gap-s24">
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
