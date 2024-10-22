<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import BasicInputField from "$lib/components/forms/fields/basic-input-field.svelte";
  import RichTextField from "$lib/components/forms/fields/rich-text-field.svelte";
  import TextareaField from "$lib/components/forms/fields/textarea-field.svelte";
  import type { Model, Service, ServicesOptions } from "$lib/types";
  import { getModelInputProps } from "$lib/utils/forms";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";

  export let servicesOptions: ServicesOptions, service: Service;
  export let model: Model | undefined = undefined;
  export let noTopPadding = false;

  let fullDesc;

  function handleUseModelValue(fieldName: string) {
    service[fieldName] = model ? model[fieldName] : undefined;
    if (fieldName === "fullDesc") {
      fullDesc.updateValue(service.fullDesc);
    }
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

  <FieldModel {...fieldModelProps.name ?? {}}>
    <BasicInputField
      id="name"
      bind:value={service.name}
      description="140 caractères maximum"
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.shortDesc ?? {}}>
    <TextareaField
      id="shortDesc"
      bind:value={service.shortDesc}
      description="Courte description affichée dans les résultats de recherche. 280 caractères maximum."
    />
  </FieldModel>

  <FieldModel {...fieldModelProps.fullDesc ?? {}} paddingTop type="markdown">
    <RichTextField
      id="fullDesc"
      bind:this={fullDesc}
      placeholder="Cette description sera affichée sur la fiche du service et permettra aux professionnels de mieux comprendre les spécificités et la valeur du service proposé. N’hésitez pas à inclure des liens, des documents à télécharger ou des vidéos explicatives. "
      vertical
      bind:value={service.fullDesc}
      description="Décrivez de manière exhaustive le service."
    />
  </FieldModel>
</FieldSet>
