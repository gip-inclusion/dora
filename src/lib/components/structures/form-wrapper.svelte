<script>
  import { setContext } from "svelte";

  import { goto } from "$app/navigation";

  import { modifyStructure, createStructure } from "$lib/structures.js";

  import structureSchema from "$lib/schemas/structure.js";
  import {
    validate,
    formErrors,
    injectAPIErrors,
    contextValidationKey,
  } from "$lib/validation.js";

  import SchemaField from "$lib/components/forms/schema-field.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";

  import Alert from "$lib/components/forms/alert.svelte";
  import { arrowRightSIcon } from "$lib/icons";

  import Button from "$lib/components/button.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";

  export let structure, structuresOptions, formTitle;

  export let modify = false;
  export let visible;
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

        resolve();
      }, 200);
    });
  }

  setContext(contextValidationKey, {
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

{#if visible}
  <form novalidate on:submit|preventDefault={handleSubmit}>
    <FieldSet title={formTitle}>
      <div slot="help">
        <p class="text-f14">
          Vérifiez l’exactitude des informations récupérées et complétez les
          autres.
        </p>
      </div>
      <div bind:this={errorDiv}>
        {#each $formErrors.nonFieldErrors || [] as msg}
          <Alert label={msg} />
        {/each}
      </div>

      <SchemaField
        type="text"
        label="Siret"
        schema={structureSchema.siret}
        name="siret"
        errorMessages={$formErrors.siret}
        disabled
        bind:value={structure.siret}
      />

      <SchemaField
        type="text"
        label="Nom"
        schema={structureSchema.name}
        name="name"
        errorMessages={$formErrors.name}
        bind:value={structure.name}
      />

      <SchemaField
        type="select"
        label="Typologie"
        placeholder="Sélectionner"
        schema={structureSchema.typology}
        sortSelect
        name="typology"
        errorMessages={$formErrors.typology}
        bind:value={structure.typology}
        choices={structuresOptions.typologies}
      />

      <SchemaField
        name="city"
        type="custom"
        label="Ville"
        errorMessages={$formErrors.city}
        schema={structureSchema.city}
      >
        <CitySearch
          slot="custom-input"
          name="city"
          placeholder="Saisissez et validez votre ville"
          initialValue={structure.city}
          onChange={handleCityChange}
          vertical
        />
      </SchemaField>

      <SchemaField
        type="custom"
        name="address1"
        label="Adresse"
        errorMessages={$formErrors.address1}
        schema={structureSchema.address1}
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

      <SchemaField
        type="text"
        label="Complément d’adresse"
        schema={structureSchema.address2}
        name="address2"
        errorMessages={$formErrors.address2}
        bind:value={structure.address2}
      />

      <SchemaField
        type="text"
        label="Code postal"
        schema={structureSchema.postalCode}
        name="postalCode"
        errorMessages={$formErrors.postalCode}
        bind:value={structure.postalCode}
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
      />

      <SchemaField
        type="tel"
        label="Téléphone"
        schema={structureSchema.phone}
        name="phone"
        errorMessages={$formErrors.phone}
        bind:value={structure.phone}
      />

      <SchemaField
        type="email"
        label="Courriel"
        schema={structureSchema.email}
        name="email"
        errorMessages={$formErrors.email}
        bind:value={structure.email}
      />

      <SchemaField
        type="url"
        label="Site web"
        placeholder="https://mastructure.fr"
        schema={structureSchema.url}
        name="url"
        errorMessages={$formErrors.url}
        bind:value={structure.url}
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
      />
      <SchemaField
        type="richtext"
        label="Présentation"
        description="Présentation résumée des missions de votre structure"
        placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
        schema={structureSchema.fullDesc}
        name="fullDesc"
        errorMessages={$formErrors.fullDesc}
        bind:value={structure.fullDesc}
        vertical
      />

      <SchemaField
        type="hidden"
        schema={structureSchema.ape}
        name="ape"
        bind:value={structure.ape}
      />

      <hr />

      <div class="flex justify-end">
        <Button
          on:submit
          name="validate"
          type="submit"
          label="Valider"
          icon={arrowRightSIcon}
          iconOnRight
          preventDefaultOnMouseDown
        />
      </div>
    </FieldSet>
  </form>
{/if}
