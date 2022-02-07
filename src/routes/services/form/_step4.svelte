<script>
  import { onMount } from "svelte";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";
  import { getStructure } from "$lib/structures";

  export let servicesOptions, service;

  function handleCityChange(city) {
    const props = city?.properties;
    service.city = props?.name;
    service.cityCode = props?.citycode;
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
  let promise;
  if (!service.city && !service.address1 && !service.postalCode) {
    promise = getStructure(service.structure);
    promise.then((structure) => {
      service.city = structure.city;
      service.address1 = structure.address1;
      service.address2 = structure.address2;
      service.postalCode = structure.postalCode;
      service.cityCode = structure.cityCode;
      service.latitude = structure.latitude;
      service.longitude = structure.longitude;
    });
  } else {
    promise = Promise.resolve();
  }
  let isTimeLimited;

  onMount(() => {
    isTimeLimited = !!service.suspensionDate;
  });

  function handleCheckTimeLimited(evt) {
    const checked = evt.target.checked;
    if (!checked) {
      service.suspensionDate = null;
    }
  }
</script>

{#await promise then structure}
  <FieldSet title="Contact">
    <ModelField
      label="Nom du contact"
      placeholder="Prénom et nom"
      type="text"
      schema={serviceSchema.contactName}
      name="contactName"
      errorMessages={$formErrors.contactName}
      bind:value={service.contactName}
    >
      <FieldHelp slot="helptext" title="Contact référent">
        Merci de préciser les coordonnées de la personne responsable de la
        réception et du traitement des demandes d’orientation. À défaut,
        renseignez le courriel et le numéro de téléphone de votre structure.Par
        défaut, ces informations sont disponibles uniquement aux accompagnateurs
        qui ont un compte DORA. En cochant la case « Rendre les informations
        publiques », les informations seront rendues disponibles à tous les
        visiteurs du site.
      </FieldHelp></ModelField
    >
    <ModelField
      type="tel"
      label="Numéro de téléphone"
      placeholder="05 ou 06 00 00 00 00"
      schema={serviceSchema.contactPhone}
      name="contactPhone"
      errorMessages={$formErrors.contactPhone}
      bind:value={service.contactPhone}
    />
    <ModelField
      type="email"
      label="Courriel"
      placeholder="Votre adresse e-mail"
      schema={serviceSchema.contactEmail}
      name="contactEmail"
      errorMessages={$formErrors.contactEmail}
      bind:value={service.contactEmail}
    />
    <ModelField
      label="Rendre les informations publiques"
      type="toggle"
      schema={serviceSchema.isContactInfoPublic}
      name="isContactInfoPublic"
      errorMessages={$formErrors.isContactInfoPublic}
      bind:value={service.isContactInfoPublic}
    />
  </FieldSet>

  <FieldSet title="Lieu">
    <ModelField
      type="checkboxes"
      label="Lieu de déroulement"
      schema={serviceSchema.locationKinds}
      name="locationKinds"
      errorMessages={$formErrors.locationKinds}
      bind:value={service.locationKinds}
      choices={servicesOptions.locationKinds}
    >
      <FieldHelp slot="helptext" title="Lieu de déroulement">
        Merci de préciser si le service ou l’accompagnement se déroule en
        présentiel ou bien à distance. Si c’est à distance, merci de préciser le
        lien de la visioconférence.
      </FieldHelp></ModelField
    >
    <ModelField
      placeholder="https://"
      type="url"
      label="Lien visioconférence"
      visible={service.locationKinds.includes("RE")}
      schema={serviceSchema.remoteUrl}
      name="remoteUrl"
      errorMessages={$formErrors.remoteUrl}
      bind:value={service.remoteUrl}
    />

    <Field
      type="custom"
      label="Ville"
      errorMessages={$formErrors.city}
      schema={serviceSchema.city}
    >
      <CitySearch
        slot="custom-input"
        name="city"
        placeholder="Saisissez et validez votre ville"
        initialValue={service.city}
        handleChange={handleCityChange}
      />
    </Field>

    <Field
      type="custom"
      label="Adresse"
      errorMessages={$formErrors.address1}
      schema={serviceSchema.address1}
    >
      <AddressSearch
        slot="custom-input"
        name="address1"
        disabled={!service.cityCode}
        cityCode={service.cityCode}
        placeholder="Saisissez et validez votre adresse"
        initialValue={service.address1}
        handleChange={handleAddressChange}
      />
    </Field>
    <ModelField
      type="text"
      label="Complément d’adresse"
      placeholder="Compléments d’adresse"
      schema={serviceSchema.address2}
      name="address2"
      errorMessages={$formErrors.address2}
      bind:value={service.address2}
    />
    <ModelField
      type="text"
      label="Code postal"
      placeholder="Code postal"
      schema={serviceSchema.postalCode}
      name="postalCode"
      errorMessages={$formErrors.postalCode}
      bind:value={service.postalCode}
    />
    <ModelField
      type="hidden"
      schema={serviceSchema.cityCode}
      name="cityCode"
      errorMessages={$formErrors.cityCode}
      bind:value={service.cityCode}
    />
    <ModelField
      type="hidden"
      schema={serviceSchema.longitude}
      name="longitude"
      errorMessages={$formErrors.longitude}
      bind:value={service.longitude}
    />
    <ModelField
      type="hidden"
      schema={serviceSchema.latitude}
      name="latitude"
      errorMessages={$formErrors.latitude}
      bind:value={service.latitude}
    />
  </FieldSet>

  <FieldSet title="Désactivation automatique">
    <ModelField
      label="Votre service est limité dans le temps ?"
      type="toggle"
      name="isTimeLimited"
      bind:value={isTimeLimited}
      on:change={handleCheckTimeLimited}
    >
      <FieldHelp slot="helptext" title="Suspension">
        En configurant la suspension de votre service avec une limite de temps,
        vous pouvez mieux gérer sa visibilité et sa mise à jour.
      </FieldHelp></ModelField
    >
    <ModelField
      label="Oui, à partir d’une date :"
      type="date"
      vertical
      schema={serviceSchema.suspensionDate}
      name="suspensionDate"
      errorMessages={$formErrors.suspensionDate}
      bind:value={service.suspensionDate}
      visible={isTimeLimited}
    />
  </FieldSet>
{/await}
