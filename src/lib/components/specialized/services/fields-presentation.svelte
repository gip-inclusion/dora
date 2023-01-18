<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/inputs/basic-input-field.svelte";
  import RichTextField from "$lib/components/inputs/rich-text-field.svelte";
  import TextareaField from "$lib/components/inputs/textarea-field.svelte";
  import type { Model } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "./field-model.svelte";

  export let servicesOptions, schema, service;
  export let model: Model | undefined = undefined;
  export let noTopPadding = false;

  let fullDesc;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
    if (fieldName === "fullDesc") {
      fullDesc.updateValue(service.fullDesc);
    }
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

  $: showModel = !!service.model;
</script>

<FieldSet title="Présentation" {showModel} {noTopPadding}>
  <div slot="help">
    <p class="text-f14">
      Le <b>Résumé</b> présente le service en une phrase courte. Il apparait dans
      les résultats de recherche.
    </p>
    <p class="text-f14">
      <strong>Exemple</strong> :
      <i>
        Faciliter vos déplacements en cas de reprise d’emploi ou de formation
        (entretien d’embauche, concours public…)
      </i>
    </p>
    <p class="text-f14">
      Si besoin, détaillez dans la partie
      <b>Description</b>.
    </p>
  </div>

  <FieldModel {...fieldModelProps["name"]}>
    <BasicInputField
      id="name"
      schema={schema.name}
      placeholder="Titre du service"
      bind:value={service.name}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps["shortDesc"]}>
    <TextareaField
      id="shortDesc"
      schema={schema.shortDesc}
      placeholder="Compléter"
      bind:value={service.shortDesc}
    />
  </FieldModel>

  <FieldModel {...fieldModelProps["fullDesc"]} paddingTop type="markdown">
    <RichTextField
      id="fullDesc"
      schema={schema.fullDesc}
      bind:this={fullDesc}
      placeholder="Informations concernant le service et ses spécificités."
      vertical
      bind:value={service.fullDesc}
    />
  </FieldModel>
</FieldSet>
