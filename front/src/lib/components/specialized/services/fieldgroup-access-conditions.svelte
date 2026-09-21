<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import { currentSchema } from "$lib/validation/validation";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";
  import { isNotFreeService } from "$lib/utils/service";
  import UploadField from "$lib/components/forms/fields/upload-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";

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

<FieldGroup title="Conditions d’accès">
  <FieldModel {...fieldModelProps.conditionsAcces ?? {}}>
    <TextareaField
      id="conditionsAcces"
      bind:value={
        () => service.conditionsAcces ?? "",
        (v) => (service.conditionsAcces = v)
      }
      description="Y a-t-il des pré-requis ou justificatifs à fournir pour accéder au service&#8239;?"
      placeholder="Exemple&#8239;: Être bénéficiaire du RSA…"
    />
  </FieldModel>
  <FieldModel {...fieldModelProps.forms ?? {}} type="files">
    <UploadField
      id="forms"
      structureSlug={service.structure}
      {onblur}
      descriptionText="Taille maximale&nbsp;: 5 Mo. Formats supportés&nbsp;: doc, docx, pdf, png, jpeg, jpg, odt, xls, xlsx, ods"
      bind:fileKeys={service.forms}
    />
  </FieldModel>
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
</FieldGroup>
