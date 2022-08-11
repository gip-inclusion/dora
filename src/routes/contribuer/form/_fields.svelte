<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import { contribSchema } from "$lib/schemas/service.js";
  import StructureSearch from "$lib/components/structures/search.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import { moveToTheEnd, orderAndReformatSubcategories } from "$lib/utils";
  import Notice from "$lib/components/notice.svelte";
  import Button from "$lib/components/button.svelte";
  import { tick } from "svelte";

  export let servicesOptions, service;
  let establishment = null;

  let subcategories = [];
  let showServiceAddress = true;

  function handleCategoriesChange(categories) {
    subcategories = categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          categories.some((category) => value.startsWith(category))
        )
      : [];
    subcategories = orderAndReformatSubcategories(
      subcategories,
      categories,
      servicesOptions
    );

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((category) => scat.startsWith(category))
    );
  }

  function handleStructureCityChange() {
    service.siret = "";
  }

  async function handleEstablishmentChange(newEstablishment) {
    service.siret = newEstablishment?.siret;
  }

  function handleCityChange(city) {
    service.city = city?.name;
    service.cityCode = city?.code;
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

  async function fillAdress() {
    showServiceAddress = false;
    if (establishment) {
      const {
        city,
        address1,
        address2,
        postalCode,
        cityCode,
        latitude,
        longitude,
      } = establishment;
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
</script>

<StructureSearch
  onEstablishmentChange={handleEstablishmentChange}
  onCityChange={handleStructureCityChange}
  bind:establishment
/>

{#if service.siret}
  <FieldSet title="Présentation">
    <div slot="help">
      <p class="text-f14">
        Le <b>Résumé</b> présente le service en une phrase courte. Il apparait dans
        les résultats de recherche.
      </p>
      <p class="text-f14">
        <strong>Exemple</strong> :
        <i>
          Faciliter vos déplacements en cas de reprise d’emploi ou de formation
          (entretien d’embauche, concours public…)
        </i>
      </p>
      <p class="text-f14">
        Si besoin, détaillez dans la partie
        <b>Description</b>.
      </p>
    </div>

    <SchemaField
      label="Nom"
      type="text"
      placeholder="Ex. Aide aux frais liés à…"
      schema={contribSchema.name}
      name="name"
      errorMessages={$formErrors.name}
      bind:value={service.name}
    />

    <SchemaField
      description="280 caractères maximum"
      placeholder="Décrivez brièvement ce service"
      type="textarea"
      label="Résumé"
      schema={contribSchema.shortDesc}
      name="shortDesc"
      errorMessages={$formErrors.shortDesc}
      bind:value={service.shortDesc}
    />

    <SchemaField
      label="Description"
      placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant ce service et ses spécificités."
      type="richtext"
      vertical
      schema={contribSchema.fullDesc}
      name="fullDesc"
      errorMessages={$formErrors.fullDesc}
      bind:value={service.fullDesc}
    />

    <SchemaField
      type="toggle"
      label="Service cumulable"
      schema={contribSchema.isCumulative}
      name="isCumulative"
      errorMessages={$formErrors.isCumulative}
      bind:value={service.isCumulative}
    />
  </FieldSet>

  <FieldSet title="Typologie">
    <div slot="help">
      <p class="text-f14">
        Classez le service par thématiques et besoins pour faciliter son
        référencement.
      </p>
    </div>
    <SchemaField
      type="multiselect"
      label="Thématiques"
      schema={contribSchema.categories}
      bind:value={service.categories}
      choices={servicesOptions.categories}
      name="categories"
      errorMessages={$formErrors.categories}
      onSelectChange={handleCategoriesChange}
      placeholderMulti="Choisissez la ou les thématiques"
      sortSelect
    />

    <SchemaField
      type="multiselect"
      label="Besoin(s) auxquels ce service répond"
      schema={contribSchema.subcategories}
      name="subcategories"
      errorMessages={$formErrors.subcategories}
      bind:value={service.subcategories}
      choices={subcategories}
      placeholder="Choisissez les sous-catégories"
      placeholderMulti="Choisissez les sous-catégories"
    />

    <SchemaField
      type="checkboxes"
      label="Type de service"
      schema={contribSchema.kinds}
      name="kinds"
      errorMessages={$formErrors.kinds}
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
      description="Quelle est la nature de ce service."
    />
  </FieldSet>

  <div class="mt-s48">
    <Notice type="warning">
      <p class="text-f14">
        Renseignez le courriel du référent afin de faciliter la validation de
        votre suggestion.
      </p>
    </Notice>
  </div>

  <FieldSet title="Contact du référent">
    <div slot="help">
      <p class="text-f14">
        Coordonnées de la personne responsable de la réception et du traitement
        des demandes d’orientation. À défaut, renseignez le courriel et le
        numéro de téléphone de la structure.
      </p>
    </div>

    <SchemaField
      label="Prénom et nom"
      placeholder="Prénom et nom"
      type="text"
      schema={contribSchema.contactName}
      name="contactName"
      errorMessages={$formErrors.contactName}
      bind:value={service.contactName}
    />
    <SchemaField
      type="tel"
      label="Numéro de téléphone"
      placeholder="05 ou 06 00 00 00 00"
      schema={contribSchema.contactPhone}
      name="contactPhone"
      errorMessages={$formErrors.contactPhone}
      bind:value={service.contactPhone}
    />
    <SchemaField
      type="email"
      label="Courriel"
      placeholder="Courriel de la personne à contacter"
      schema={contribSchema.contactEmail}
      name="contactEmail"
      errorMessages={$formErrors.contactEmail}
      bind:value={service.contactEmail}
    />
  </FieldSet>

  <div class="mt-s48">
    <Notice title="Informations facultatives">
      <p class="text-f14">
        Les informations ci-dessous sont facultatives, mais facilitent le
        travail des structures porteuses.
      </p>
    </Notice>
  </div>

  <FieldSet title="Publics">
    <div slot="help">
      <p class="text-f14">Publics auxquels le service s’adresse.</p>
    </div>

    <SchemaField
      type="multiselect"
      label="Profils"
      description="Plusieurs choix possibles"
      schema={contribSchema.concernedPublic}
      name="concernedPublic"
      errorMessages={$formErrors.concernedPublic}
      bind:value={service.concernedPublic}
      choices={servicesOptions.concernedPublic}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
      sortSelect
    />

    <SchemaField
      type="multiselect"
      label="Critères"
      description="Plusieurs choix possibles"
      schema={contribSchema.accessConditions}
      name="accessConditions"
      errorMessages={$formErrors.accessConditions}
      bind:value={service.accessConditions}
      choices={servicesOptions.accessConditions}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
      sortSelect
    />

    <SchemaField
      type="multiselect"
      description="Plusieurs choix possibles"
      schema={contribSchema.requirements}
      name="requirements"
      errorMessages={$formErrors.requirements}
      bind:value={service.requirements}
      choices={servicesOptions.requirements}
      label="Pré-requis ou compétences"
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
      sortSelect
    />

    <SchemaField
      type="toggle"
      label="Frais à charge du bénéficiaire"
      schema={contribSchema.hasFee}
      name="hasFee"
      errorMessages={$formErrors.hasFee}
      bind:value={service.hasFee}
    />

    {#if !!service.hasFee}
      <SchemaField
        type="textarea"
        hideLabel
        placeholder="Adhésion, frais de location, frais de garde, etc., et les montants."
        schema={contribSchema.feeDetails}
        name="feeDetails"
        errorMessages={$formErrors.feeDetails}
        bind:value={service.feeDetails}
      />
    {/if}
  </FieldSet>

  <FieldSet title="Accueil">
    <SchemaField
      type="checkboxes"
      label={contribSchema.locationKinds.name}
      schema={contribSchema.locationKinds}
      name="locationKinds"
      errorMessages={$formErrors.locationKinds}
      bind:value={service.locationKinds}
      choices={moveToTheEnd(
        servicesOptions.locationKinds,
        "value",
        "a-distance"
      )}
    />
    {#if service.locationKinds.includes("a-distance")}
      <SchemaField
        placeholder="https://"
        type="url"
        label="Lien visioconférence"
        schema={contribSchema.remoteUrl}
        name="remoteUrl"
        errorMessages={$formErrors.remoteUrl}
        bind:value={service.remoteUrl}
      />
    {/if}

    {#if service.locationKinds.includes("en-presentiel")}
      <Button
        on:click={fillAdress}
        secondary
        small
        label="Utiliser l'adresse de la structure"
      />

      {#if showServiceAddress}
        <Field type="custom" label="Ville" errorMessages={$formErrors.city}>
          <CitySearch
            slot="custom-input"
            name="city"
            placeholder="Saisissez et validez votre ville"
            initialValue={service.city}
            onChange={handleCityChange}
          />
        </Field>

        <Field
          type="custom"
          label="Adresse"
          errorMessages={$formErrors.address1}
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

        <SchemaField
          type="text"
          label="Complément d’adresse"
          placeholder="Compléments d’adresse"
          schema={contribSchema.address2}
          name="address2"
          errorMessages={$formErrors.address2}
          bind:value={service.address2}
        />

        <SchemaField
          type="text"
          label="Code postal"
          placeholder="Code postal"
          schema={contribSchema.postalCode}
          name="postalCode"
          errorMessages={$formErrors.postalCode}
          bind:value={service.postalCode}
        />

        <SchemaField
          type="hidden"
          schema={contribSchema.cityCode}
          name="cityCode"
          errorMessages={$formErrors.cityCode}
          bind:value={service.cityCode}
        />

        <SchemaField
          type="hidden"
          schema={contribSchema.longitude}
          name="longitude"
          errorMessages={$formErrors.longitude}
          bind:value={service.longitude}
        />

        <SchemaField
          type="hidden"
          schema={contribSchema.latitude}
          name="latitude"
          errorMessages={$formErrors.latitude}
          bind:value={service.latitude}
        />
      {/if}
    {/if}
  </FieldSet>
{/if}
