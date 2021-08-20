<script>
  import { onMount, setContext } from "svelte";

  import { goto } from "$app/navigation";

  import {
    structureOptions,
    fillStructuresOptions,
    modifyStructure,
    createStructure,
  } from "$lib/structures.js";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import structureSchema from "$lib/schemas/structure.js";
  import {
    validate,
    formErrors,
    injectAPIErrors,
    contextValidationKey,
  } from "$lib/validation.js";

  import ValidateButton from "./_validate.svelte";

  export let formTitle;

  export let structure;
  export let modify = false;
  export let visible;

  function handleBlur(elt) {
    const schema = structureSchema.pick([elt.target.name]);
    const validatedData = validate(structure, schema);
    if (validatedData) {
      structure = { ...structure, ...validatedData };
    }
  }

  setContext(contextValidationKey, {
    onBlur: handleBlur,
  });

  const serverErrors = {
    _default: {},
    siret: { unique: "Cette structure existe déjà" },
  };

  async function handleSubmit() {
    const validatedData = validate(structure, structureSchema);
    if (validatedData) {
      // Validation OK, let's send it to the API endpoint
      let result;
      if (modify) {
        result = await modifyStructure(validatedData);
      } else {
        result = await createStructure(validatedData);
      }
      if (result?.ok) {
        goto(`/structures/${result.result.slug}`);
      } else {
        injectAPIErrors(result.error, serverErrors);
      }
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

{#if $structureOptions && visible}
  <form novalidate on:submit|preventDefault={handleSubmit}>
    <FieldSet title={formTitle}>
      <ModelField
        type="text"
        label="SIRET"
        field={$structureOptions.siret}
        name="siret"
        errorMessage={$formErrors.siret}
        disabled
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
        name="name"
        errorMessage={$formErrors.name}
        bind:value={structure.name}
        vertical />
      <ModelField
        type="select"
        label="Typologie de la structure"
        placeholder="choisissez"
        field={$structureOptions.typology}
        name="typology"
        errorMessage={$formErrors.typology}
        bind:value={structure.typology}
        bind:selectedItem={structure._typology}
        vertical />
      <ModelField
        type="text"
        label="Adresse"
        field={$structureOptions.address1}
        name="address1"
        errorMessage={$formErrors.address1}
        bind:value={structure.address1}
        vertical />
      <ModelField
        type="text"
        label="Complément d’adresse"
        field={$structureOptions.address2}
        name="address2"
        errorMessage={$formErrors.address2}
        bind:value={structure.address2}
        vertical />
      <div class="flex flex-row justify-between gap-x-4">
        <div class="w-20">
          <ModelField
            type="text"
            label="Code postal"
            field={$structureOptions.postalCode}
            name="postalCode"
            errorMessage={$formErrors.postalCode}
            bind:value={structure.postalCode}
            vertical />
        </div>
        <div class="flex-auto">
          <ModelField
            type="text"
            label="Ville"
            field={$structureOptions.city}
            name="city"
            errorMessage={$formErrors.city}
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
            name="phone"
            errorMessage={$formErrors.phone}
            bind:value={structure.phone}
            vertical />
        </div>

        <div class="flex-auto">
          <ModelField
            type="email"
            label="Courriel"
            field={$structureOptions.email}
            name="email"
            errorMessage={$formErrors.email}
            bind:value={structure.email}
            vertical />
        </div>
      </div>
      <ModelField
        type="url"
        label="Site web"
        placeholder="https://mastructure.fr"
        field={$structureOptions.url}
        name="url"
        errorMessage={$formErrors.url}
        bind:value={structure.url}
        vertical />
      <ModelField
        type="textarea"
        label="Résumé"
        description="280 caractères maximum"
        placeholder="Décrivez brièvement votre structure"
        field={$structureOptions.shortDesc}
        name="shortDesc"
        errorMessage={$formErrors.shortDesc}
        bind:value={structure.shortDesc} />
      <ModelField
        type="richtext"
        label="Présentez votre structure"
        description="Présentation résumée des missions de votre structure"
        placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
        field={$structureOptions.fullDesc}
        name="fullDesc"
        errorMessage={$formErrors.fullDesc}
        bind:value={structure.fullDesc}
        vertical />

      <ModelField
        type="hidden"
        field={$structureOptions.cityCode}
        name="cityCode"
        bind:value={structure.cityCode}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.ape}
        name="ape"
        bind:value={structure.ape}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.longitude}
        name="longitude"
        bind:value={structure.longitude}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.latitude}
        name="latitude"
        bind:value={structure.latitude}
        vertical />

      <div class="border-b border-gray-01" />

      <div class="self-end">
        <ValidateButton _disabled={false} />
      </div>
    </FieldSet>
  </form>
{/if}
