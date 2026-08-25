<script lang="ts">
  import { untrack } from "svelte";

  import FieldSet from "$lib/components/display/fieldset.svelte";
  import Notice from "$lib/components/display/notice.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import RadioButtonsField from "$lib/components/forms/fields/radio-buttons-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import { isNotFreeService } from "$lib/utils/service";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { currentSchema } from "$lib/validation/validation";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
    model?: Model;
  }

  let { servicesOptions, service = $bindable(), model }: Props = $props();

  service.mobilisationModes ??= [];
  service.mobilisableBy ??= [];
  service.mobilisationLink ??= "";
  service.mobilisationDetails ??= "";

  function handleUseModelValue(fieldName) {
    service[fieldName] = model ? model[fieldName] : undefined;
    service = { ...service };
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
    if (!service.mobilisationModes?.includes("utiliser-lien-mobilisation")) {
      untrack(() => {
        service.mobilisationLink = "";
      });
    }
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
    title="Modalités d’orientation"
    showIcon={false}
    titleLevel="h3"
  >
    Afin que le service puisse être mobilisable, merci de choisir qui peut le
    mobiliser.
  </Notice>

  <FieldModel {...fieldModelProps.mobilisableBy ?? {}} type="array">
    <CheckboxesField
      id="mobilisableBy"
      bind:value={service.mobilisableBy}
      choices={servicesOptions.mobilisableBy}
      description="Plusieurs choix possibles."
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.mobilisationModes ?? {}} type="array">
    <CheckboxesField
      id="mobilisationModes"
      bind:value={service.mobilisationModes}
      choices={servicesOptions.mobilisationModes}
      description="Plusieurs choix possibles."
    />
  </FieldModel>

  {#if service.mobilisationModes?.includes("utiliser-lien-mobilisation")}
    <FieldModel {...fieldModelProps.mobilisationLink ?? {}}>
      <BasicInputField
        id="mobilisationLink"
        type="url"
        descriptionText="Laissez vide pour utiliser le formulaire DORA. Format attendu : https://exemple.fr"
        bind:value={service.mobilisationLink}
      />
    </FieldModel>
  {/if}

  <FieldModel {...fieldModelProps.mobilisationDetails ?? {}}>
    <TextareaField
      id="mobilisationDetails"
      description="Précisions libres, par exemple un mode « autre »."
      bind:value={service.mobilisationDetails}
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
</FieldSet>
