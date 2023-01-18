<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import CheckboxesField from "$lib/components/inputs/checkboxes-field.svelte";
  import MultiSelectField from "$lib/components/inputs/multi-select-field.svelte";
  import ToggleField from "$lib/components/inputs/toggle-field.svelte";
  import type { Model } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import type { Schema } from "$lib/validation/schemas/utils";

  import FieldCategory from "./field-category.svelte";
  import FieldModel from "./field-model.svelte";

  export let servicesOptions, schema: Schema, service;
  export let model: Model | undefined = undefined;
  export let noTopPadding = false;
  export let subcategories = [];
  let showModelSubcategoriesUseButton = true;

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

<FieldSet title="Typologie" {showModel} {noTopPadding}>
  <FieldModel {...fieldModelProps["categories"]} type="array">
    <FieldCategory
      bind:service
      bind:subcategories
      {servicesOptions}
      {model}
      {schema}
    />
  </FieldModel>
  <div slot="help">
    <p class="text-f14">
      Classez le service par thématiques et besoins pour faciliter son
      référencement.
    </p>
  </div>

  <FieldModel
    {...fieldModelProps["subcategories"]}
    showUseButton={showModelSubcategoriesUseButton}
    type="array"
  >
    <MultiSelectField
      id="subcategories"
      schema={schema.subcategories}
      bind:value={service.subcategories}
      choices={subcategories}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
    />
  </FieldModel>
  <FieldModel {...fieldModelProps["kinds"]} type="array">
    <CheckboxesField
      id="kinds"
      schema={schema.kinds}
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps["isCumulative"]} type="boolean">
    <ToggleField
      id="isCumulative"
      schema={schema.isCumulative}
      bind:value={service.isCumulative}
      description="Avec d’autres services."
    />
  </FieldModel>
</FieldSet>
