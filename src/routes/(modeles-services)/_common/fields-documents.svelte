<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AddableMultiSelectField from "$lib/components/forms/fields/addable-multiselect-field.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import UploadField from "$lib/components/forms/fields/upload-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";

  export let servicesOptions: ServicesOptions, service: Service;
  export let model: Model | undefined = undefined;

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

<FieldSet title="Documents" {showModel}>
  <div slot="help">
    <p class="text-f14">
      Justificatifs à fournir et documents à compléter pour postuler. Le lien
      redirige vers une page web qui présente le service (formulaire, fiche de
      prescription, simulateurs, etc.)
    </p>
  </div>

  <FieldModel {...fieldModelProps.forms ?? {}} type="files">
    <UploadField
      id="forms"
      structureSlug={service.structure}
      on:blur
      bind:fileKeys={service.forms}
    />
  </FieldModel>

  {#if servicesOptions.credentials.length}
    <FieldModel {...fieldModelProps.credentials ?? {}} type="array">
      <AddableMultiSelectField
        id="credentials"
        bind:values={service.credentials}
        structureSlug={service.structure}
        choices={servicesOptions.credentials}
        placeholder="Aucun"
        placeholderMulti="Choisir un autre justificatif"
        sort
        addButtonLabel="Ajouter un autre justificatif"
      />
    </FieldModel>
  {/if}

  <FieldModel {...fieldModelProps.onlineForm ?? {}}>
    <BasicInputField
      id="onlineForm"
      placeholder="URL"
      type="url"
      bind:value={service.onlineForm}
    />
  </FieldModel>
</FieldSet>
