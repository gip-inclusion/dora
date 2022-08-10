<script>
  import { tick, setContext } from "svelte";

  import {
    formErrors,
    validate,
    contextValidationKey,
  } from "$lib/validation.js";
  import { moveToTheEnd } from "$lib/utils";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";
  import Button from "$lib/components/button.svelte";

  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import AdminDivisionSearch from "$lib/components/forms/admin-division-search.svelte";

  export let servicesOptions, serviceSchema, service, structure;

  let adminDivisionChoices = [];

  function handleCityChange(city) {
    service.city = city?.name;
    service.cityCode = city?.code;
  }

  function handleDiffusionZoneTypeChange(type) {
    if (type !== service.diffusionZoneType) {
      service.diffusionZoneType = type;
      service.diffusionZoneDetails = "";
      service.diffusionZoneDetailsDisplay = "";
      adminDivisionChoices = [];
    }
  }

  function handlediffusionZoneDetailsChange(details) {
    service.diffusionZoneDetails = details;
  }

  function handleAddressChange(address) {
    const props = address?.properties;
    const coords = address?.geometry.coordinates;
    const lat = coords?.[1];
    const long = coords?.[0];
    service.address1 = props?.name;
    service.postalCode = props?.postcode;
    service.longitude = long;
    service.latitude = lat;
  }

  let showServiceAddress = true;

  async function fillAdress() {
    showServiceAddress = false;

    if (structure) {
      const {
        city,
        address1,
        address2,
        postalCode,
        cityCode,
        latitude,
        longitude,
      } = structure;
      service.city = city;
      service.address1 = address1;
      service.address2 = address2;
      service.postalCode = postalCode;
      service.cityCode = cityCode;
      service.latitude = latitude;
      service.longitude = longitude;
    }
    await tick();
    showServiceAddress = true;
  }

  async function handleEltChange(evt) {
    // We want to listen to both DOM and component events
    const fieldname = evt.target?.name || evt.detail;

    // Sometimes (particularly with Select components), the event is received
    // before the field value is updated in `service`, although it's not
    // supposed to happen. This setTimeout is a unsatisfying workaround to that.
    await new Promise((resolve) => {
      setTimeout(() => {
        const filteredSchema = {
          // si le champs n'existe pas dans le schéma,
          // on l'initialise avec une valeur par défaut
          [fieldname]: serviceSchema[fieldname] || { rules: [] },
        };

        const { validatedData, valid } = validate(service, filteredSchema, {
          fullSchema: serviceSchema,
          noScroll: true,
          extraData: servicesOptions,
        });

        if (valid) {
          service = { ...service, ...validatedData };
        }

        resolve();
      }, 200);
    });
  }

  setContext(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });
</script>

<FieldSet title="Périmètre géographique d’intervention" noTopPadding>
  <div slot="help">
    <p class="text-f14">
      Qu’il soit national, régional, départemental, intercommunal ou communal,
      le service peut être délimité aux bénéficiaires habitant sur un territoire
      spécifique.
    </p>

    <h5 class="mb-s0">QPV et ZRR</h5>
    <p class="text-f14">
      Activez cette option si votre offre s’adresse uniquement aux bénéficiaires
      résidants dans des Quartiers Prioritaires de la politique de la Ville ou
      des Zones de Revitalisation Rurale.
    </p>
  </div>
  <SchemaField
    type="select"
    label={serviceSchema.diffusionZoneType.name}
    schema={serviceSchema.diffusionZoneType}
    choices={servicesOptions.diffusionZoneType}
    name="diffusionZoneType"
    errorMessages={$formErrors.diffusionZoneType}
    onSelectChange={handleDiffusionZoneTypeChange}
    initialValue={service.diffusionZoneTypeDisplay}
  />

  {#if service.diffusionZoneType !== "country"}
    <SchemaField
      type="custom"
      name="diffusionZoneDetails"
      label={serviceSchema.diffusionZoneDetails.name}
      description="Commencez à saisir le nom et choisissez dans la liste."
      errorMessages={$formErrors.diffusionZoneDetails}
      schema={serviceSchema.diffusionZoneDetails}
    >
      <AdminDivisionSearch
        slot="custom-input"
        name="diffusionZoneDetails"
        searchType={service.diffusionZoneType}
        handleChange={handlediffusionZoneDetailsChange}
        initialValue={service.diffusionZoneDetailsDisplay}
        bind:choices={adminDivisionChoices}
      />
    </SchemaField>
  {/if}

  <SchemaField
    label={serviceSchema.qpvOrZrr.name}
    type="toggle"
    name="qpvOrZrr"
    schema={serviceSchema.qpvOrZrr}
    errorMessages={$formErrors.qpvOrZrr}
    bind:value={service.qpvOrZrr}
  />
</FieldSet>

<FieldSet title="Accueil">
  <SchemaField
    type="checkboxes"
    label={serviceSchema.locationKinds.name}
    schema={serviceSchema.locationKinds}
    name="locationKinds"
    errorMessages={$formErrors.locationKinds}
    bind:value={service.locationKinds}
    choices={moveToTheEnd(servicesOptions.locationKinds, "value", "a-distance")}
  />

  {#if service.locationKinds.includes("a-distance")}
    <SchemaField
      placeholder="https://"
      type="url"
      label={serviceSchema.remoteUrl.name}
      schema={serviceSchema.remoteUrl}
      name="remoteUrl"
      errorMessages={$formErrors.remoteUrl}
      bind:value={service.remoteUrl}
    />
  {/if}

  {#if service.locationKinds.includes("en-presentiel")}
    <Button
      on:click={fillAdress(structure)}
      secondary
      small
      label="Utiliser l'adresse de la structure"
    />

    {#if showServiceAddress}
      <SchemaField
        name="city"
        type="custom"
        label={serviceSchema.city.name}
        errorMessages={$formErrors.city}
        schema={serviceSchema.city}
      >
        <CitySearch
          slot="custom-input"
          name="city"
          placeholder="Saisissez et validez votre ville"
          initialValue={service.city}
          onChange={handleCityChange}
        />
      </SchemaField>

      <SchemaField
        type="custom"
        name="address1"
        label={serviceSchema.address1.name}
        errorMessages={$formErrors.address1}
        schema={serviceSchema.address1}
      >
        <AddressSearch
          slot="custom-input"
          name="address1"
          disabled={!service.cityCode}
          cityCode={service.cityCode}
          placeholder="3 rue du parc"
          initialValue={service.address1}
          handleChange={handleAddressChange}
        />
      </SchemaField>

      <SchemaField
        type="text"
        label={serviceSchema.address2.name}
        placeholder="batiment, escalier, etc."
        schema={serviceSchema.address2}
        name="address2"
        errorMessages={$formErrors.address2}
        bind:value={service.address2}
      />

      <SchemaField
        type="text"
        label={serviceSchema.postalCode.name}
        placeholder="00000"
        schema={serviceSchema.postalCode}
        name="postalCode"
        errorMessages={$formErrors.postalCode}
        bind:value={service.postalCode}
      />

      <SchemaField
        type="hidden"
        schema={serviceSchema.cityCode}
        name="cityCode"
        errorMessages={$formErrors.cityCode}
        bind:value={service.cityCode}
      />

      <SchemaField
        type="hidden"
        schema={serviceSchema.longitude}
        name="longitude"
        errorMessages={$formErrors.longitude}
        bind:value={service.longitude}
      />

      <SchemaField
        type="hidden"
        schema={serviceSchema.latitude}
        name="latitude"
        errorMessages={$formErrors.latitude}
        bind:value={service.latitude}
      />
    {/if}
  {/if}
</FieldSet>

<FieldSet title="Contact">
  <div slot="help">
    <p class="text-f14">
      Coordonnées de la personne responsable de la réception et du traitement
      des demandes d’orientation. À défaut, renseignez le courriel et le numéro
      de téléphone de votre structure.
    </p>
    <p class="text-f14">
      Par défaut, ces informations sont disponibles uniquement aux
      accompagnateurs qui ont un compte DORA. En cochant la case « Rendre
      public », les informations seront rendues disponibles à tous les visiteurs
      du site.
    </p>
  </div>
  <SchemaField
    label={serviceSchema.contactName.name}
    placeholder="Prénom et nom"
    type="text"
    schema={serviceSchema.contactName}
    name="contactName"
    errorMessages={$formErrors.contactName}
    bind:value={service.contactName}
  />
  <SchemaField
    type="tel"
    label={serviceSchema.contactPhone.name}
    placeholder="00 00 00 00 00"
    schema={serviceSchema.contactPhone}
    name="contactPhone"
    errorMessages={$formErrors.contactPhone}
    bind:value={service.contactPhone}
  />
  <SchemaField
    type="email"
    label={serviceSchema.contactEmail.name}
    placeholder="nom@exemple.org"
    schema={serviceSchema.contactEmail}
    name="contactEmail"
    errorMessages={$formErrors.contactEmail}
    bind:value={service.contactEmail}
  />
  <SchemaField
    label={serviceSchema.isContactInfoPublic.name}
    type="toggle"
    schema={serviceSchema.isContactInfoPublic}
    name="isContactInfoPublic"
    errorMessages={$formErrors.isContactInfoPublic}
    bind:value={service.isContactInfoPublic}
  />
</FieldSet>
