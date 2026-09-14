<script lang="ts">
  import FieldGroup from "$lib/components/display/field-group.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RichTextField from "$lib/components/forms/fields/rich-text-field.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import { getModelInputProps } from "$lib/utils/forms";
  import { currentSchema } from "$lib/validation/validation";
  import type { FieldGroupProps } from "$lib/components/specialized/services/types.ts";

  let {
    servicesOptions,
    service = $bindable(),
    model,
  }: FieldGroupProps = $props();

  let description: RichTextField;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
    if (fieldName === "description") {
      description.updateValue(service.description);
    }
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
</script>

<FieldGroup title="Presentation">
  <FieldModel {...fieldModelProps.name ?? {}}>
    <BasicInputField
      id="name"
      bind:value={service.name}
      descriptionText="Entre 3 à 150 caractères. Écriture en minuscules recommandée, sauf pour les acronymes."
      placeholder="Titre du service…"
    />
  </FieldModel>
  <FieldModel {...fieldModelProps.description ?? {}} paddingTop type="markdown">
    <RichTextField
      id="description"
      bind:this={description}
      placeholder="Décrivez simplement le service"
      vertical
      bind:value={service.description}
      description="Privilégier des phrases courtes et un langage simple. Idéalement entre 200 et 2000 caractères. Cette description sera affichée sur la fiche du service et permettra aux utilisateurs de mieux comprendre le service proposé."
    />
  </FieldModel>
</FieldGroup>
