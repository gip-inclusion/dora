<script lang="ts">
  import { goto } from "$app/navigation";
  import Alert from "$lib/components/display/alert.svelte";
  import Button from "$lib/components/display/button.svelte";
  import LinkButton from "$lib/components/display/link-button.svelte";
  import SchemaField from "$lib/components/inputs/schema-field.svelte";
  import CitySearch from "$lib/components/specialized/city-search.svelte";
  import OpeningHoursField from "$lib/components/specialized/openingHours/opening-hours-field.svelte";
  import AddressSearch from "$lib/components/specialized/street-search.svelte";
  import { createStructure, modifyStructure } from "$lib/requests/structures";
  import type { Structure, StructuresOptions } from "$lib/types";
  import { getDepartmentFromCityCode } from "$lib/utils/misc";
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
  export let onRefresh = undefined;

  let errorDiv;

  async function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldName = evt.target?.name || evt.detail;

    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in  `structure`, although it's not
    // supposed to happen. This setTimeout is an unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
        const filteredSchema =
          fieldName && structureSchema[fieldName]
            ? { [fieldName]: structureSchema[fieldName] }
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

  function getAccessLibreUrl(structure) {
    const department = getDepartmentFromCityCode(structure.cityCode);
    const where = encodeURIComponent(`${structure.city} (${department})`);
    const lat = encodeURIComponent(structure.latitude);
    const long = encodeURIComponent(structure.longitude);
    const code = encodeURIComponent(structure.cityCode);
    return `https://acceslibre.beta.gouv.fr/recherche/?what=&where=${where}&lat=${lat}&lon=${long}&code=${code}`;
  }

  $: accesslibreUrl = getAccessLibreUrl(structure);
</script>

<form
  novalidate
  on:submit|preventDefault={handleSubmit}
  class="flex flex-col gap-s32 rounded-md border border-gray-02 bg-white p-s32 lg:w-2/3"
>
  {#if $formErrors.nonFieldErrors && $formErrors.nonFieldErrors.length}
    <div bind:this={errorDiv}>
      {#each $formErrors.nonFieldErrors || [] as msg}
        <Alert id="global-errors" label={msg} />
      {/each}
    </div>
  {/if}

  <SchemaField
    type="text"
    label="SIRET"
    schema={structureSchema.siret}
    name="siret"
    errorMessages={$formErrors.siret}
    disabled
    bind:value={structure.siret}
    vertical
  />

  <SchemaField
    type="text"
    label="Nom de la structure"
    placeholder="Plateforme de l’inclusion"
    schema={structureSchema.name}
    name="name"
    errorMessages={$formErrors.name}
    bind:value={structure.name}
    vertical
  />

  <SchemaField
    type="select"
    label="Typologie"
    placeholder="Choisissez…"
    schema={structureSchema.typology}
    sortSelect
    name="typology"
    errorMessages={$formErrors.typology}
    bind:value={structure.typology}
    choices={structuresOptions.typologies}
    vertical
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
      placeholder="Paris"
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
      placeholder="127 rue de Grenelle"
      initialValue={structure.address1}
      handleChange={handleAddressChange}
    />
  </SchemaField>

  <SchemaField
    type="text"
    label="Complément d’adresse"
    placeholder="étage, bâtiment…"
    schema={structureSchema.address2}
    name="address2"
    errorMessages={$formErrors.address2}
    bind:value={structure.address2}
    vertical
  />

  <SchemaField
    type="text"
    label="Code postal"
    placeholder="75007"
    schema={structureSchema.postalCode}
    name="postalCode"
    errorMessages={$formErrors.postalCode}
    bind:value={structure.postalCode}
    vertical
  />

  <SchemaField
    type="hidden"
    schema={structureSchema.cityCode}
    name="cityCode"
    errorMessages={$formErrors.cityCode}
    bind:value={structure.cityCode}
  />

  <SchemaField
    type="hidden"
    schema={structureSchema.longitude}
    name="longitude"
    errorMessages={$formErrors.longitude}
    bind:value={structure.longitude}
  />
  <SchemaField
    type="hidden"
    schema={structureSchema.latitude}
    name="latitude"
    errorMessages={$formErrors.latitude}
    bind:value={structure.latitude}
    vertical
  />

  <SchemaField
    type="url"
    label="Accessibilité"
    description="Afin de renseigner les informations d’accessibilité sur la structure, retrouvez-la via la plateforme <a class='underline text-magenta-cta' href='{accesslibreUrl}' target='_blank' title='Ouverture dans une nouvelle fenêtre' rel='noopener'>accès libre</a> et copiez l’url dans le champs ci-dessous"
    placeholder="https://acceslibre.beta.gouv.fr/…"
    schema={structureSchema.accesslibreUrl}
    name="accesslibreUrl"
    errorMessages={$formErrors.accesslibreUrl}
    bind:value={structure.accesslibreUrl}
    vertical
    htmlDescription
  />

  <SchemaField
    type="tel"
    label="Téléphone"
    schema={structureSchema.phone}
    name="phone"
    errorMessages={$formErrors.phone}
    bind:value={structure.phone}
    vertical
  />

  <SchemaField
    type="email"
    label="Courriel"
    placeholder="nom.prenom@organisation.fr"
    schema={structureSchema.email}
    name="email"
    errorMessages={$formErrors.email}
    bind:value={structure.email}
    vertical
  />

  <SchemaField
    type="url"
    label="Site web"
    placeholder="https://mastructure.fr"
    schema={structureSchema.url}
    name="url"
    errorMessages={$formErrors.url}
    bind:value={structure.url}
    vertical
  />

  <SchemaField
    type="textarea"
    label="Résumé"
    description="280 caractères maximum"
    placeholder="Décrivez brièvement votre structure"
    schema={structureSchema.shortDesc}
    name="shortDesc"
    errorMessages={$formErrors.shortDesc}
    bind:value={structure.shortDesc}
    vertical
  />

  <SchemaField
    type="richtext"
    label="Présentation"
    placeholder="Présentation détaillée de la structure"
    schema={structureSchema.fullDesc}
    name="fullDesc"
    errorMessages={$formErrors.fullDesc}
    bind:value={structure.fullDesc}
    vertical
  />

  <SchemaField
    type="multiselect"
    label="Labels nationaux"
    name="nationalLabels"
    description="Indiquez si la structure fait partie d'un ou plusieurs réseaux nationaux"
    placeholder="Choisissez…"
    placeholderMulti="Choisissez…"
    schema={structureSchema.nationalLabels}
    errorMessages={$formErrors.nationalLabels}
    bind:value={structure.nationalLabels}
    choices={structuresOptions.nationalLabels}
    vertical
  />

  <SchemaField
    type="text"
    name="otherLabels"
    label="Autres labels"
    description="Indiquez si la structure fait partie d’autres labels (régionaux, locaux…)"
    schema={structureSchema.otherLabels}
    errorMessages={$formErrors.otherLabels}
    bind:value={structure.otherLabels}
    vertical
  />

  <SchemaField
    type="hidden"
    schema={structureSchema.ape}
    name="ape"
    errorMessages={$formErrors.ape}
    bind:value={structure.ape}
  />

  <OpeningHoursField
    label="Horaires de la structure"
    name="openingHours"
    on:change={handleEltChange}
    errorMessages={$formErrors.openingHours}
    bind:value={structure.openingHours}
  />

  <SchemaField
    type="text"
    label="Détail horaires"
    description="Vous pouvez renseigner des informations spécifiques concernant les horaires dans ce champ"
    placeholder=""
    schema={structureSchema.openingHoursDetails}
    name="openingHoursDetails"
    errorMessages={$formErrors.openingHoursDetails}
    bind:value={structure.openingHoursDetails}
    vertical
  />

  <hr />

  <div class="flex flex-col justify-end gap-s16 md:flex-row ">
    <LinkButton
      to="/structures/{structure.slug}"
      on:submit
      secondary
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
