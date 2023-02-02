<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import CheckboxesField from "$lib/components/forms/fields/checkboxes-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldCategory from "./field-category.svelte";
  import FieldModel from "./field-model.svelte";
  import FieldSubcategory from "./field-subcategory.svelte";

  export let servicesOptions: ServicesOptions, service: Service;
  export let model: Model | undefined = undefined;
  export let noTopPadding = false;

  $: showModel = !!service.model;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
  }

  $: fieldModelProps = model
    ? getModelInputProps({
        service,
        servicesOptions,
        showModel,
        onUseModelValue: handleUseModelValue,
        model,
      })
    : {};
</script>

<FieldSet title="Typologie" {showModel} {noTopPadding}>
  <FieldModel {...fieldModelProps.categories ?? {}} type="array">
    <FieldCategory bind:service {servicesOptions} {model} />
  </FieldModel>
  <div slot="help">
    <p class="text-f14">
      Classez le service par thématiques et besoins pour faciliter son
      référencement.
    </p>
  </div>

  <FieldModel
    {...fieldModelProps.subcategories ?? {}}
    showUseButton
    type="array"
  >
    <FieldSubcategory bind:service {servicesOptions} />
  </FieldModel>
  <FieldModel {...fieldModelProps.kinds ?? {}} type="array">
    <CheckboxesField
      id="kinds"
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.isCumulative ?? {}} type="boolean">
    <BooleanRadioButtonsField
      id="isCumulative"
      bind:value={service.isCumulative}
      description="Avec d’autres services."
    />
  </FieldModel>
</FieldSet>
