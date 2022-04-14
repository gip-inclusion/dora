<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service-contrib.js";
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import Info from "$lib/components/forms/form-info.svelte";

  export let servicesOptions;
  export let service;
  export let establishment;

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

  service.city = establishment.city;
  service.address1 = establishment.address1;
  service.address2 = establishment.address2;
  service.postalCode = establishment.postalCode;
  service.cityCode = establishment.cityCode;
  service.latitude = establishment.latitude;
  service.longitude = establishment.longitude;
</script>

<Info title="Informations non obligatoires">
  Vous avez décidé de rajouter des informations supplémentaires concernant le
  service saisi. Ces informations ne sont pas obligatoires, mais nous permettent
  d’enregistrer des informations qualifiées et ainsi de faciliter le travail des
  structures porteuses. Renseignez ce que vous connaissez et cliquez sur
  «&nbsp;Envoyer la contribution&nbsp;».
</Info>

<FieldSet title="Conditions d'accès pour le bénéficiaire">
  <ModelField
    type="multiselect"
    label="Critères d’accès"
    description="Précisez les critères d’éligibilité du public afin de recevoir des orientations adéquates. Plusieurs choix possibles."
    schema={serviceSchema.accessConditions}
    name="accessConditions"
    errorMessages={$formErrors.accessConditions}
    bind:value={service.accessConditions}
    choices={servicesOptions.accessConditions}
    placeholder="Aucun critère spécifique"
    placeholderMulti="Choisir un autre critères d’admission"
    sortSelect
  >
    <FieldHelp slot="helptext" title="Critères d’éligibilité">
      <p>Définissez le type de publics auxquels ce service s’adresse.</p>
      <p>
        Si le service est ouvert à tout le monde, sans critères ou prérequis,
        laissez les champs avec les options par défaut.
      </p>
    </FieldHelp>
  </ModelField>

  <ModelField
    type="multiselect"
    label="Publics concernés"
    description="Ces critères permettent d’orienter le bon public vers ce service. Plusieurs choix possibles."
    schema={serviceSchema.concernedPublic}
    name="concernedPublic"
    errorMessages={$formErrors.concernedPublic}
    bind:value={service.concernedPublic}
    choices={servicesOptions.concernedPublic}
    placeholder="Tous publics"
    placeholderMulti="Choisir un autre type de publics"
    sortSelect
  />

  <ModelField
    type="multiselect"
    label="Quels sont les pré-requis ou compétences ?"
    description="Plusieurs choix possibles."
    schema={serviceSchema.requirements}
    name="requirements"
    errorMessages={$formErrors.requirements}
    bind:value={service.requirements}
    choices={servicesOptions.requirements}
    placeholder="Aucun"
    placeholderMulti="Choisir un autre pré-requis"
    sortSelect
  />

  <ModelField
    type="toggle"
    label="Service cumulable"
    description="Ce service est cumulable avec d’autres services ? "
    schema={serviceSchema.isCumulative}
    name="isCumulative"
    errorMessages={$formErrors.isCumulative}
    bind:value={service.isCumulative}
  />
  <ModelField
    type="toggle"
    label="Frais à charge du bénéficiaire"
    schema={serviceSchema.hasFee}
    name="hasFee"
    errorMessages={$formErrors.hasFee}
    bind:value={service.hasFee}
  />

  <ModelField
    type="textarea"
    hideLabel
    placeholder="Merci de détailler ici les frais à charge du bénéficiaire : adhésion, frais de location, frais de garde, etc., et les montants."
    visible={!!service.hasFee}
    schema={serviceSchema.feeDetails}
    name="feeDetails"
    errorMessages={$formErrors.feeDetails}
    bind:value={service.feeDetails}
  />
</FieldSet>

<FieldSet title="Personne à contacter">
  <ModelField
    label="Nom du contact"
    placeholder="Prénom et nom"
    type="text"
    schema={serviceSchema.contactName}
    name="contactName"
    errorMessages={$formErrors.contactName}
    bind:value={service.contactName}
  >
    <FieldHelp slot="helptext" title="Contact">
      Si vous les connaissez, merci de renseigner les coordonnées de la personne
      responsable de la réception et du traitement des demandes d’orientation,
      pour ce service. À défaut, renseignez le courriel et le numéro de
      téléphone de la personne avec qui vous êtes en contact.
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
    placeholder="Courriel de la personne à contacter"
    schema={serviceSchema.contactEmail}
    name="contactEmail"
    errorMessages={$formErrors.contactEmail}
    bind:value={service.contactEmail}
  />
</FieldSet>

<FieldSet title="Lieu de déroulement">
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
    visible={service.locationKinds.includes("a-distance")}
    schema={serviceSchema.remoteUrl}
    name="remoteUrl"
    errorMessages={$formErrors.remoteUrl}
    bind:value={service.remoteUrl}
  />

  <Field type="custom" label="Ville" errorMessages={$formErrors.city}>
    <CitySearch
      slot="custom-input"
      name="city"
      placeholder="Saisissez et validez votre ville"
      initialValue={service.city}
      handleChange={handleCityChange}
    />
  </Field>

  <Field type="custom" label="Adresse" errorMessages={$formErrors.address1}>
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
