<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import { structureOptions, fillStructuresOptions } from "$lib/structures.js";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import structSchema from "$lib/schemas/structure.js";

  import ValidateButton from "./_validate.svelte";
  import { submit } from "./submit.js";

  export let formTitle;

  export let structure;
  export let modify = false;

  let theForm;
  let formErrors = {};
  let formIsValid = false;

  const serverErrors = {
    _default: {},
    siret: { unique: "Cette structure existe déjà" },
  };

  function handleChange() {
    formIsValid = theForm.checkValidity();
  }

  function displayYupErrors(errors) {
    formErrors = {};
    Object.entries(errors).forEach(([fieldName, message]) => {
      formErrors[fieldName] = message;
    });
    formErrors = formErrors;
  }

  function displayAPIErrors(errors) {
    formErrors = {};
    Object.entries(errors).forEach(([key, values]) => {
      const fieldName = key;
      values.forEach((value) => {
        const errorCode = value.code;
        const errorMessage =
          (serverErrors[fieldName] && serverErrors[fieldName][errorCode]) ||
          serverErrors._default[errorCode] ||
          value.message;
        // TODO append instead of overwrite; there might be more than one error
        // by field
        formErrors[fieldName] = errorMessage;
      });
    });
    formErrors = formErrors;
  }

  async function handleSubmit() {
    let errors = {};
    try {
      structSchema.validateSync(structure, { abortEarly: false });
    } catch (err) {
      errors = err.inner.reduce(
        (acc, e) => ({ ...acc, [e.path]: e.message }),
        {}
      );
      displayYupErrors(errors);
      return;
    }
    // Validation OK, let's send it to the API endpoint
    const result = await submit(structure, modify);
    if (result.ok) {
      goto(`/structures/${result.result.slug}`);
    } else {
      displayAPIErrors(result.error);
    }
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

{#if $structureOptions}
  <form
    novalidate
    on:change={handleChange}
    on:submit|preventDefault={handleSubmit}
    on:input={handleChange}
    bind:this={theForm}>
    <FieldSet title={formTitle}>
      <ModelField
        type="text"
        label="SIRET"
        field={$structureOptions.siret}
        errorMessage={formErrors.siret}
        disabled={false}
        bind:value={structure.siret}
        vertical>
        <FieldHelp title="Completez les informations" slot="helptext">
          <p>
            Vérifiez l’exactitude des informations récupérées et complétez les
            autres.
          </p>
        </FieldHelp>
      </ModelField>

      <ModelField
        type="text"
        label="Nom de la structure"
        field={$structureOptions.name}
        errorMessage={formErrors.name}
        bind:value={structure.name}
        vertical />
      <ModelField
        type="select"
        label="Typologie de la structure"
        placeholder="choisissez"
        field={$structureOptions.typology}
        errorMessage={formErrors.typology}
        bind:value={structure.typology}
        bind:selectedItem={structure._typology}
        vertical />
      <ModelField
        type="text"
        label="Adresse"
        field={$structureOptions.address1}
        errorMessage={formErrors.address1}
        bind:value={structure.address1}
        vertical />
      <ModelField
        type="text"
        label="Complément d’adresse"
        field={$structureOptions.address2}
        errorMessage={formErrors.address2}
        bind:value={structure.address2}
        vertical />
      <div class="flex flex-row justify-between gap-x-4">
        <div class="w-20">
          <ModelField
            type="text"
            label="Code postal"
            field={$structureOptions.postalCode}
            errorMessage={formErrors.postalCode}
            bind:value={structure.postalCode}
            vertical />
        </div>
        <div class="flex-auto">
          <ModelField
            type="text"
            label="Ville"
            field={$structureOptions.city}
            errorMessage={formErrors.city}
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
            errorMessage={formErrors.phone}
            bind:value={structure.phone}
            vertical />
        </div>

        <div class="flex-auto">
          <ModelField
            type="email"
            label="Courriel"
            field={$structureOptions.email}
            errorMessage={formErrors.email}
            bind:value={structure.email}
            vertical />
        </div>
      </div>
      <ModelField
        type="url"
        label="Site web"
        placeholder="https://mastructure.fr"
        field={$structureOptions.url}
        errorMessage={formErrors.url}
        bind:value={structure.url}
        vertical />
      <ModelField
        type="textarea"
        label="Résumé"
        description="280 caractères maximum"
        placeholder="Décrivez brièvement votre structure"
        field={$structureOptions.shortDesc}
        errorMessage={formErrors.shortDesc}
        bind:value={structure.shortDesc} />
      <ModelField
        type="richtext"
        label="Présentez votre structure"
        description="Présentation résumée des missions de votre structure"
        placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
        field={$structureOptions.fullDesc}
        errorMessage={formErrors.fullDesc}
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
{/if}
