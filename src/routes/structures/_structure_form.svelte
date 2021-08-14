<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import { structureOptions, fillStructuresOptions } from "$lib/structures.js";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";

  import ValidateButton from "./_validate.svelte";
  import { submit } from "./submit.js";

  export let formTitle;
  export let theForm;
  export let structure;
  export let modify = false;

  let formErrors = {};
  let formIsValid = false;

  function handleChange() {
    formIsValid = theForm.checkValidity();
  }

  async function handleSubmit() {
    const result = await submit(structure, modify);
    if (result.ok) {
      goto(`/structures/${result.result.slug}`);
    } else {
      displayErrors(result.error);
    }
    console.log(result.error);
  }

  function displayErrors(errors) {
    formErrors = {};
    Object.entries(errors).forEach(([key, values]) => {
      let fieldName = key;
      values.forEach((value) => {
        let errorCode = value.code;
        let errorMessage = value.message;
        // TODO append instead of overwrite; there might be more than one error
        // by field
        formErrors[fieldName] = { errorCode, errorMessage };
        formErrors = formErrors;
      });
    });
  }

  function getTypologyItem() {
    return structure.typology
      ? $structureOptions.typology.choices.find(
          (choice) => choice.value === structure.typology
        )
      : null;
  }

  $: structure._typology = $structureOptions ? getTypologyItem() : null;

  onMount(async () => {
    await fillStructuresOptions();
  });
</script>

<form
  on:change={handleChange}
  on:submit|preventDefault={handleSubmit}
  on:input={handleChange}
  bind:this={theForm}>
  <FieldSet title={formTitle}>
    <ModelField
      type="text"
      label="SIRET"
      field={$structureOptions.siret}
      errors={formErrors.siret}
      errorMessages={{ unique: "Cette structure existe déjà" }}
      disabled
      bind:value={structure.siret}
      vertical>
      <FieldHelp title="Completez les informations" slot="helptext">
        <p>
          Vérifiez l’exactitude des informations récupérées et complétez les
          autres.
        </p>
      </FieldHelp></ModelField>

    <ModelField
      type="text"
      label="Nom de la structure"
      field={$structureOptions.name}
      errors={formErrors.name}
      bind:value={structure.name}
      vertical />
    <ModelField
      type="select"
      label="Typologie de la structure"
      placeholder="choisissez"
      field={$structureOptions.typology}
      errors={formErrors.typology}
      bind:value={structure.typology}
      bind:selectedItem={structure._typology}
      vertical />
    <ModelField
      type="text"
      label="Adresse"
      field={$structureOptions.address1}
      errors={formErrors.address1}
      bind:value={structure.address1}
      vertical />
    <ModelField
      type="text"
      label="Complément d’adresse"
      field={$structureOptions.address2}
      errors={formErrors.address2}
      bind:value={structure.address2}
      vertical />
    <div class="flex flex-row justify-between gap-x-4">
      <div class="w-20">
        <ModelField
          type="text"
          label="Code postal"
          field={$structureOptions.postalCode}
          errors={formErrors.postalCode}
          bind:value={structure.postalCode}
          vertical />
      </div>
      <div class="flex-auto">
        <ModelField
          type="text"
          label="Ville"
          field={$structureOptions.city}
          errors={formErrors.city}
          bind:value={structure.city}
          vertical />
      </div>
    </div>
    <div class="flex flex-row justify-between gap-x-4 ">
      <div class="flex-auto">
        <ModelField
          type="tel"
          label="Téléphone"
          field={$structureOptions.phone}
          errors={formErrors.phone}
          bind:value={structure.phone}
          vertical />
      </div>

      <div class="flex-auto">
        <ModelField
          type="email"
          label="Courriel"
          field={$structureOptions.email}
          errors={formErrors.email}
          bind:value={structure.email}
          vertical />
      </div>
    </div>
    <ModelField
      type="url"
      label="Site web"
      placeholder="https://mastructure.fr"
      field={$structureOptions.url}
      errors={formErrors.url}
      bind:value={structure.url}
      vertical />
    <ModelField
      type="textarea"
      label="Résumé"
      description="280 caractères maximum"
      placeholder="Décrivez brièvement votre structure"
      field={$structureOptions.shortDesc}
      errors={formErrors.shortDesc}
      bind:value={structure.shortDesc} />
    <ModelField
      type="richtext"
      label="Présentez votre structure"
      description="Présentation résumée des missions de votre structure"
      placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
      field={$structureOptions.fullDesc}
      errors={formErrors.fullDesc}
      bind:value={structure.fullDesc}
      vertical />

    <ModelField
      type="hidden"
      field={$structureOptions.cityCode}
      bind:value={structure.cityCode}
      vertical />
    <ModelField
      type="hidden"
      field={$structureOptions.ape}
      bind:value={structure.ape}
      vertical />
    <ModelField
      type="hidden"
      field={$structureOptions.longitude}
      bind:value={structure.longitude}
      vertical />
    <ModelField
      type="hidden"
      field={$structureOptions.latitude}
      bind:value={structure.latitude}
      vertical />

    <div class="border-b border-gray-01" />

    <div class="self-end">
      <ValidateButton _disabled={!formIsValid} />
    </div>
  </FieldSet>
</form>
