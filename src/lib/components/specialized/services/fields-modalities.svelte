<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/inputs/checkboxes-field.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";
  import TextareaField from "$lib/components/inputs/textarea-field.svelte";
  import type { Model } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import { moveToTheEnd } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldModel from "./field-model.svelte";

  export let servicesOptions, schema, service;
  export let model: Model | undefined = undefined;

  $: showModel = !!service.model;

  function handleUseModelValue(fieldName) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: fieldModelProps = model
    ? getModelInputProps({
        schema,
        service,
        servicesOptions,
        showModel,
        onUseModelValue: handleUseModelValue,
        model,
      })
    : {};
</script>

<FieldSet title="Modalités" {showModel}>
  <div slot="help">
    <p class="text-f14">Modalités pour mobiliser le service.</p>
  </div>

  <div class="flex flex-col lg:gap-s8">
    <FieldModel {...fieldModelProps["coachOrientationModes"]} type="array">
      <CheckboxesField
        id="coachOrientationModes"
        schema={schema.coachOrientationModes}
        choices={moveToTheEnd(
          servicesOptions.coachOrientationModes,
          "value",
          "autre"
        )}
        bind:value={service.coachOrientationModes}
      />
    </FieldModel>

    {#if service.coachOrientationModes.includes("autre")}
      <FieldModel {...fieldModelProps["coachOrientationModesOther"]}>
        <BasicInputField
          id="coachOrientationModesOther"
          schema={schema.coachOrientationModesOther}
          hideLabel
          placeholder="Compléter"
          bind:value={service.coachOrientationModesOther}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="flex flex-col lg:gap-s8">
    <FieldModel {...fieldModelProps["beneficiariesAccessModes"]} type="array">
      <CheckboxesField
        id="beneficiariesAccessModes"
        schema={schema.beneficiariesAccessModes}
        choices={moveToTheEnd(
          servicesOptions.beneficiariesAccessModes,
          "value",
          "autre"
        )}
        bind:value={service.beneficiariesAccessModes}
      />
    </FieldModel>

    {#if service.beneficiariesAccessModes.includes("autre")}
      <FieldModel {...fieldModelProps["beneficiariesAccessModesOther"]}>
        <BasicInputField
          id="beneficiariesAccessModesOther"
          schema={schema.beneficiariesAccessModesOther}
          hideLabel
          placeholder="Merci de préciser la modalité"
          bind:value={service.beneficiariesAccessModesOther}
        />
      </FieldModel>
    {/if}
  </div>

  <div class="flex flex-col gap-s4">
    <FieldModel
      {...fieldModelProps["feeCondition"]}
      serviceValue={service.feeCondition}
      type="text"
    >
      <SelectField
        id="feeCondition"
        schema={schema.feeCondition}
        placeholder="Choisissez…"
        bind:value={service.feeCondition}
        choices={servicesOptions.feeConditions.filter(
          (fee) => fee.value !== "pass-numerique"
        )}
      />
    </FieldModel>

    {#if isNotFreeService(service.feeCondition)}
      <FieldModel {...fieldModelProps["feeDetails"]}>
        <TextareaField
          id="feeDetails"
          schema={schema.feeDetails}
          placeholder="Merci de détailler ici les frais à charge du bénéficiaire : adhésion, frais de location, frais de garde, etc., et les montants."
          bind:value={service.feeDetails}
        />
      </FieldModel>
    {/if}
  </div>
</FieldSet>
