<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";

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

  let autoSuspend;

  $: if (service.suspensionCount || service.suspensionDate) {
    autoSuspend = true;
  }
</script>

<FieldSet title="Personne à contacter">
  <ModelField
    label="Nom du contact"
    placeholder="Prénom et nom"
    type="text"
    schema={serviceSchema.contactName}
    name="contactName"
    errorMessages={$formErrors.contactName}
    bind:value={service.contactName}>
    <FieldHelp slot="helptext" title="Contact référent">
      Merci de préciser les coordonnées de la personne en charge de ce service.
    </FieldHelp></ModelField>
  <ModelField
    type="tel"
    label="Numéro de téléphone"
    placeholder="05 ou 06 00 00 00 00"
    schema={serviceSchema.contactPhone}
    name="contactPhone"
    errorMessages={$formErrors.contactPhone}
    bind:value={service.contactPhone} />
  <ModelField
    type="email"
    label="Courriel"
    placeholder="Votre adresse e-mail"
    schema={serviceSchema.contactEmail}
    name="contactEmail"
    errorMessages={$formErrors.contactEmail}
    bind:value={service.contactEmail} />
  <ModelField
    label="Rendre les informations publiques"
    type="toggle"
    schema={serviceSchema.isContactInfoPublic}
    name="isContactInfoPublic"
    errorMessages={$formErrors.isContactInfoPublic}
    bind:value={service.isContactInfoPublic} />
</FieldSet>

<FieldSet title="Lieu">
  <ModelField
    type="checkboxes"
    label="Lieu de déroulement"
    schema={serviceSchema.locationKinds}
    name="locationKinds"
    errorMessages={$formErrors.locationKinds}
    bind:value={service.locationKinds}
    choices={servicesOptions.locationKinds}>
    <FieldHelp slot="helptext" title="Lieu de déroulement">
      Merci de préciser si le service ou l’accompagnement se déroule en
      présentiel ou bien à distance. Si c’est à distance, merci de préciser le
      lien de la visioconférence.
    </FieldHelp></ModelField>
  <ModelField
    placeholder="https://"
    type="url"
    label="Lien visioconférence"
    visible={service.locationKinds.includes("RE")}
    schema={serviceSchema.remoteUrl}
    name="remoteUrl"
    errorMessages={$formErrors.remoteUrl}
    bind:value={service.remoteUrl} />

  <Field
    type="custom"
    label="Ville"
    errorMessages={$formErrors.city}
    schema={serviceSchema.city}>
    <CitySearch
      slot="custom-input"
      name="city"
      placeholder="Saisissez et validez votre ville"
      initialValue={service.city}
      handleChange={handleCityChange} />
  </Field>
  <Field
    type="custom"
    label="Adresse"
    errorMessages={$formErrors.address1}
    schema={serviceSchema.address1}>
    <AddressSearch
      slot="custom-input"
      name="address1"
      disabled={!service.cityCode}
      cityCode={service.cityCode}
      placeholder="Saisissez et validez votre adresse"
      initialValue={service.address1}
      handleChange={handleAddressChange} />
  </Field>
  <ModelField
    type="text"
    label="Complément d’adresse"
    placeholder="Compléments d’adresse"
    schema={serviceSchema.address2}
    name="address2"
    errorMessages={$formErrors.address2}
    bind:value={service.address2} />
  <ModelField
    type="text"
    label="Code postal"
    placeholder="Code postal"
    schema={serviceSchema.postalCode}
    name="postalCode"
    errorMessages={$formErrors.postalCode}
    bind:value={service.postalCode} />
  <ModelField
    type="hidden"
    schema={serviceSchema.cityCode}
    name="cityCode"
    errorMessages={$formErrors.cityCode}
    bind:value={service.cityCode} />
  <ModelField
    type="hidden"
    schema={serviceSchema.longitude}
    name="longitude"
    errorMessages={$formErrors.longitude}
    bind:value={service.longitude} />
  <ModelField
    type="hidden"
    schema={serviceSchema.latitude}
    name="latitude"
    errorMessages={$formErrors.latitude}
    bind:value={service.latitude} />
</FieldSet>

<FieldSet title="Durée et modalités de disponibilité">
  <div>Votre service est limité dans le temps ?</div>
  <!-- <ModelField
    label="Votre service est limité dans le temps ?"
    type="toggle"
    field={serviceOptions.isTimeLimited}
    name="isTimeLimited"
    errorMessages={$formErrors.isTimeLimited}
    bind:value={service.isTimeLimited} /> -->
  <ModelField
    type="date"
    label="Date de début"
    schema={serviceSchema.startDate}
    name="startDate"
    errorMessages={$formErrors.startDate}
    bind:value={service.startDate}>
    <FieldHelp slot="helptext" title="Suspension">
      En configurant la suspension de votre service (avec une limite de temps ou
      de candidatures), vous pouvez mieux gérer la visibilité de votre service
      et sa mise à jour.
    </FieldHelp></ModelField>
  <ModelField
    type="date"
    label="Date de fin"
    schema={serviceSchema.endDate}
    name="endDate"
    errorMessages={$formErrors.endDate}
    bind:value={service.endDate} />
  <ModelField
    type="radios"
    label="Récurrences"
    schema={serviceSchema.recurrence}
    name="recurrence"
    errorMessages={$formErrors.recurrence}
    bind:value={service.recurrence}
    choices={servicesOptions.recurrence} />
  <ModelField
    type="text"
    placeholder="Préciser"
    hideLabel
    visible={service.recurrence === "OT"}
    schema={serviceSchema.recurrenceOther}
    name="recurrenceOther"
    errorMessages={$formErrors.recurrenceOther}
    bind:value={service.recurrenceOther} />
  <div>Critères de suspension :</div>
  <!-- <Field
    name="autoSuspend"
    type="toggle"
    label="Critères de suspension"
    bind:value={autoSuspend} /> -->
  <ModelField
    label="Oui, à partir d’un nombre d’inscriptions :"
    placeholder="Préciser le nombre maximum"
    type="number"
    minValue={1}
    schema={serviceSchema.suspensionCount}
    name="suspensionCount"
    errorMessages={$formErrors.suspensionCount}
    bind:value={service.suspensionCount} />
  <ModelField
    label="Oui, à partir d’une date :"
    type="date"
    schema={serviceSchema.suspensionDate}
    name="suspensionDate"
    errorMessages={$formErrors.suspensionDate}
    bind:value={service.suspensionDate} />
</FieldSet>
