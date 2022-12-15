<script lang="ts">
  import { goto } from "$app/navigation";
  import Alert from "$lib/components/display/alert.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import OpeningHoursField from "$lib/components/specialized/openingHours/opening-hours-field.svelte";
  import SchemaField from "$lib/components/inputs/schema-field.svelte";
  import SelectField from "$lib/components/inputs/select/select-field.svelte";
  import CitySearch from "$lib/components/specialized/city-search.svelte";
  import AddressSearch from "$lib/components/specialized/street-search.svelte";
  import TextField from "$lib/components/inputs/text-field.svelte";
  import { createStructure, modifyStructure } from "$lib/requests/structures";
  import type { Structure, StructuresOptions } from "$lib/types";
  import structureSchema from "$lib/validation/schemas/structure";
  import {
    contextValidationKey,
    formErrors,
    injectAPIErrors,
    validate,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { setContext } from "svelte";

  export let structure: Structure;
  export let structuresOptions: StructuresOptions;

  export let modify = false;
  export let onRefresh;

  let errorDiv;

  async function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;

    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in  `structure`, although it's not
    // supposed to happen. This setTimeout is a unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
        const filteredSchema =
          fieldname && structureSchema[fieldname]
            ? { [fieldname]: structureSchema[fieldname] }
            : {};

        const { validatedData, valid } = validate(structure, filteredSchema, {
          fullSchema: structureSchema,
          noScroll: true,
        });

        if (valid) {
          structure = { ...structure, ...validatedData };
        }

        resolve(true);
      }, 200);
    });
  }

  setContext<ValidationContext>(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });

  const serverErrors = {
    _default: {},
    siret: { unique: "Cette structure existe déjà" },
  };

  async function handleSubmit() {
    $formErrors = {};
    const { validatedData, valid } = validate(structure, structureSchema);
    if (valid) {
      // Validation OK, let's send it to the API endpoint
      let result;
      if (modify) {
        result = await modifyStructure(validatedData);
      } else {
        result = await createStructure(validatedData);
      }

      if (result?.ok) {
        if (modify && onRefresh) {
          await onRefresh();
        }

        goto(`/structures/${result.result.slug}`);
      } else {
        injectAPIErrors(
          result.error || {
            nonFieldErrors: [
              {
                code: "fetch-error",
                message: "Erreur de connexion au serveur",
              },
            ],
          },
          serverErrors
        );
        errorDiv.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }

  function handleCityChange(city) {
    structure.city = city?.name;
    structure.cityCode = city?.code;
  }

  function handleAddressChange(address) {
    const props = address?.properties;
    const coords = address?.geometry.coordinates;
    const lat = coords?.[1];
    const long = coords?.[0];
    structure.address1 = props?.name;
    structure.postalCode = props?.postcode;
    structure.longitude = long;
    structure.latitude = lat;
  }
</script>

<form
  novalidate
  on:submit|preventDefault={handleSubmit}
  class="flex flex-col gap-s32 rounded-t-md border border-gray-02 p-s32 lg:w-2/3"
>
  <div class="text-f14 text-gray-text">
    <span class="text-error">*</span>
    Champs obligatoires
  </div>

  {#if $formErrors.nonFieldErrors && $formErrors.nonFieldErrors.length}
    <div bind:this={errorDiv}>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert label={msg} />
      {/each}
    </div>
  {/if}

  <TextField
    name="siret"
    label="SIRET"
    on:blur={handleEltChange}
    bind:value={structure.siret}
    errorMessages={$formErrors.siret}
    maxlength={14}
    required={structureSchema.siret.required}
    disabled
    helper="Format attendu : 14 chiffres"
  />

  <TextField
    name="name"
    label="Nom de la structure"
    bind:value={structure.name}
    on:blur={handleEltChange}
    errorMessages={$formErrors.name}
    maxlength={255}
    required={structureSchema.name.required}
  />

  <SelectField
    label="Typologie"
    name="typology"
    placeholder="Choississez..."
    errorMessages={$formErrors.typology}
    bind:value={structure.typology}
    onChange={handleEltChange}
    choices={structuresOptions.typologies}
  />

  <SchemaField
    name="city"
    type="custom"
    label="Ville"
    errorMessages={$formErrors.city}
    schema={structureSchema.city}
    vertical
  >
    <CitySearch
      slot="custom-input"
      name="city"
      placeholder="Saisissez et validez votre ville"
      initialValue={structure.city}
      onChange={handleCityChange}
    />
  </SchemaField>

  <SchemaField
    type="custom"
    name="address1"
    label="Adresse"
    errorMessages={$formErrors.address1}
    schema={structureSchema.address1}
    vertical
  >
    <AddressSearch
      slot="custom-input"
      name="address1"
      disabled={!structure.cityCode}
      cityCode={structure.cityCode}
      placeholder="3 rue du parc"
      initialValue={structure.address1}
      handleChange={handleAddressChange}
    />
  </SchemaField>

  <TextField
    name="address2"
    label="Complément d’adresse"
    bind:value={structure.address2}
    on:blur={handleEltChange}
    errorMessages={$formErrors.address2}
    maxlength={255}
  />

  <TextField
    name="accesslibreUrl"
    label="Accessibilité"
    helper="Afin de renseigner les informations d’accessibilité sur la structure, retrouvez-la via la plateforme <a href='https://acceslibre.beta.gouv.fr/' target='_blank' title='Ouverture dans une nouvelle fenêtre' rel='noopener'>accès libre</a> et copiez l’url dans le champs ci-dessous"
    bind:value={structure.accesslibreUrl}
    on:blur={handleEltChange}
    placeholder="https://acceslibre.beta.gouv.fr/..."
    errorMessages={$formErrors.accesslibreUrl}
    maxlength={255}
  />

  <TextField
    inputType="text"
    label="Code postal"
    name="postalCode"
    helper="Exemple : 44000"
    on:blur={handleEltChange}
    required
    errorMessages={$formErrors.postalCode}
    bind:value={structure.postalCode}
  />

  <TextField
    label="cityCode"
    name="cityCode"
    inputType="hidden"
    bind:value={structure.cityCode}
  />
  <TextField
    label="longitude"
    name="longitude"
    inputType="hidden"
    bind:value={structure.longitude}
  />
  <TextField
    label="latitude"
    name="latitude"
    inputType="hidden"
    bind:value={structure.latitude}
  />

  <TextField
    inputType="tel"
    label="Téléphone"
    name="phone"
    on:blur={handleEltChange}
    helper="Exemples: 06 00 00 00 00 ou 0600000000"
    errorMessages={$formErrors.phone}
    bind:value={structure.phone}
  />

  <TextField
    inputType="email"
    label="Courriel"
    helper="Exemple: nom.prenom@organisation.fr"
    name="email"
    on:blur={handleEltChange}
    required={structureSchema.email.required}
    errorMessages={$formErrors.email}
    bind:value={structure.email}
  />

  <TextField
    inputType="url"
    label="Site web"
    helper="Exemple: https://mastructure.fr"
    placeholder="https://mastructure.fr"
    name="url"
    on:blur={handleEltChange}
    errorMessages={$formErrors.url}
    bind:value={structure.url}
  />

  <TextField
    inputType="textarea"
    label="Résumé"
    helper="280 caractères maximum"
    placeholder="Décrivez brièvement votre structure"
    name="shortDesc"
    maxlength={280}
    on:blur={handleEltChange}
    required={structureSchema.shortDesc.required}
    errorMessages={$formErrors.shortDesc}
    bind:value={structure.shortDesc}
  />

  <TextField
    inputType="richtext"
    label="Présentation"
    name="fullDesc"
    errorMessages={$formErrors.fullDesc}
    bind:value={structure.fullDesc}
    on:blur={handleEltChange}
    placeholder="Présentation détaillée de la structure"
  />

  <SelectField
    label="Labels nationaux"
    name="nationalLabels"
    helper="Indiquez si la structure fait partie d'un ou plusieurs réseaux nationaux"
    placeholder="Choississez..."
    errorMessages={$formErrors.nationalLabels}
    bind:value={structure.nationalLabels}
    onChange={handleEltChange}
    choices={structuresOptions.nationalLabels}
    isMultiple
  />

  <TextField
    name="otherLabels"
    label="Autres labels"
    helper="Indiquez si la structure fait partie d’autres labels (régionaux, locaux…)"
    bind:value={structure.otherLabels}
    on:blur={handleEltChange}
    errorMessages={$formErrors.otherLabels}
    maxlength={255}
  />

  <TextField
    label="ape"
    inputType="hidden"
    name="ape"
    bind:value={structure.ape}
  />

  <OpeningHoursField
    label="Horaires de la structure"
    name="openingHours"
    on:change={handleEltChange}
    errorMessages={$formErrors.openingHours}
    bind:value={structure.openingHours}
  />

  <TextField
    name="openingHoursDetails"
    label="Détail horaires"
    helper="Vous pouvez renseigner des informations spécifiques concernant les horaires dans ce champ"
    bind:value={structure.openingHoursDetails}
    on:blur={handleEltChange}
    errorMessages={$formErrors.openingHoursDetails}
    maxlength={255}
  />

  <hr />

  <div class="flex justify-end">
    <LinkButton
      to="/structures/{structure.slug}"
      on:submit
      secondary
      extraClass="mr-s16"
      label="Annuler les modifications"
    />
    <Button
      on:submit
      name="validate"
      type="submit"
      label="Valider les modifications"
    />
  </div>
</form>
