<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import MultiSelectField from "$lib/components/forms/fields/multi-select-field.svelte";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import { currentSchema } from "$lib/validation/validation";

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

<FieldGroup title="Financement" showSeparator={false}>
  {#snippet fundingLabelsDescription()}
    <small>
      Choisissez un ou plusieurs financeurs. S’il ne figure pas dans la liste,
      demandez son ajout au
      <a
        href="mailto:support.dora@inclusion.gouv.fr"
        class="accent-gray-02 underline"
        target="_blank"
        title="Ouverture dans une nouvelle fenêtre"
        rel="noopener"
      >
        support Dora
      </a>.
    </small>
  {/snippet}

  <FieldModel
    {...fieldModelProps.fundingLabels ?? {}}
    type="array"
    options={servicesOptions.fundingLabels}
  >
    <MultiSelectField
      id="fundingLabels"
      choices={servicesOptions.fundingLabels}
      bind:value={service.fundingLabels}
      descriptionSnippet={fundingLabelsDescription}
    />
  </FieldModel>
</FieldGroup>
