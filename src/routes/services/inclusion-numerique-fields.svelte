<script lang="ts">
  import Button from "$lib/components/display/button.svelte";
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import SchemaField from "$lib/components/inputs/schema-field.svelte";
  import SelectField from "$lib/components/inputs/obsolete/select-field.svelte";
  import AdminDivisionSearch from "$lib/components/specialized/admin-division-search.svelte";
  import CitySearch from "$lib/components/specialized/city-search.svelte";
  import AddressSearch from "$lib/components/specialized/street-search.svelte";
  import type { Choice, Service, ServicesOptions, Structure } from "$lib/types";
  import { moveToTheEnd, orderAndReformatSubcategories } from "$lib/utils/misc";
  import { isNotFreeService } from "$lib/utils/service";
  import {
    contextValidationKey,
    formErrors,
    validate,
    type ValidationContext,
  } from "$lib/validation/validation";
  import { onMount, setContext, tick } from "svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";

  export let servicesOptions: ServicesOptions;
  export let service: Service;
  export let structure: Structure;
  export let serviceSchema;

  let subcategories = [];

  let showServiceAddress = true;

  function existInServicesOptionsConcernedPublic(concernedPublicOption) {
    return servicesOptions.concernedPublic
      .filter(
        (genericConcernedPublicOption): boolean =>
          genericConcernedPublicOption.structure == null
      )
      .map(
        (genericConcernedPublicOption: Choice): string =>
          genericConcernedPublicOption.label
      )
      .includes(concernedPublicOption.label);
  }

  function addServicesOptionsConcernedPublicValues(concernedPublicOption: {
    label: string;
  }): Choice {
    return {
      label: concernedPublicOption.label,
      value: servicesOptions.concernedPublic.find(
        (option: Choice) => option.label === concernedPublicOption.label
      ).value,
    };
  }

  const concernedPublicOptions: Choice[] = [
    {
      label: "Familles/enfants",
      structure: null,
    },
    {
      label: "Jeunes (16-26 ans)",
      structure: null,
    },
    {
      label: "Adultes",
      structure: null,
    },
    {
      label: "Femmes",
      structure: null,
    },
    {
      label: "Seniors (+65 ans)",
      structure: null,
    },
    {
      label: "Publics langues étrangères",
      structure: null,
    },
    {
      label: "Déficience visuelle",
      structure: null,
    },
    {
      label: "Surdité",
      structure: null,
    },
    {
      label:
        "Handicaps psychiques : troubles psychiatriques donnant lieu à des atteintes comportementales",
      structure: null,
    },
    {
      label:
        "Handicaps mentaux : déficiences limitant les activités d’une personne",
      structure: null,
    },
    {
      label: "Personnes en situation d’illettrisme",
      structure: null,
    },
  ]
    .filter(existInServicesOptionsConcernedPublic)
    .map(addServicesOptionsConcernedPublicValues);

  function existInServicesOptionsKinds(kindsOption) {
    return servicesOptions.kinds
      .map((genericKindsOption: Choice): string => genericKindsOption.value)
      .includes(kindsOption.value);
  }

  const kindsOptions = [
    {
      value: "autonomie",
      label: "Seul : j’ai accès à du matériel et une connexion",
    },
    {
      value: "accompagnement",
      label:
        "Avec de l’aide : je suis accompagné seul dans l’usage du numérique",
    },
    {
      value: "atelier",
      label:
        "Dans un atelier : j’apprends collectivement à utiliser le numérique",
    },
    {
      value: "delegation",
      label:
        "À ma place : une personne habilitée fait les démarches à ma place",
    },
  ].filter(existInServicesOptionsKinds);

  function updateServicePresentation(subcategories) {
    service.name = "Médiation numérique";
    service.shortDesc = `${
      structure.name
    } propose des services : ${subcategories.slice(
      0,
      253 - structure.name.length
    )}${subcategories.length > 253 - structure.name.length ? "..." : ""}`;
  }

  function setCategories(categories = ["numerique"]) {
    subcategories = servicesOptions.subcategories.filter(({ value }) =>
      categories.some(
        (cat) => value.startsWith(cat) && value !== "numerique--autre"
      )
    );

    subcategories = orderAndReformatSubcategories(
      subcategories,
      categories,
      servicesOptions
    );

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }

  async function fillAddress() {
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
      service.postalCode = postalCode.toString();
      service.cityCode = cityCode.toString();
      service.latitude = latitude;
      service.longitude = longitude;
    }
    await tick();
    showServiceAddress = true;
  }

  service.locationKinds = [];

  function setModalites() {
    service.coachOrientationModes = ["autre"];
    service.coachOrientationModesOther =
      "Mêmes modalités que pour les bénéficiaires";
  }

  function setDiffusionZone() {
    if (!structure.latitude || !structure.longitude) return;
    service.diffusionZoneType = "department";
    service.diffusionZoneDetails = structure.department;
  }

  function setLocationKinds() {
    service.locationKinds = ["en-presentiel"];
  }

  function setContact() {
    if (structure.phone && !service.contactPhone) {
      service.contactPhone = structure.phone;
    }

    if (structure.email && !service.contactEmail) {
      service.contactEmail = structure.email;
    }
  }

  function setConcernedPublic() {
    service.concernedPublic = service.concernedPublic.filter(
      (concernedPublicValue: string): boolean =>
        concernedPublicOptions
          .map((concernedPublicOption): string => concernedPublicOption.value)
          .includes(concernedPublicValue)
    );
  }

  setCategories();
  setConcernedPublic();
  setContact();

  onMount(() => {
    setModalites();
    setDiffusionZone();
    setLocationKinds();
  });

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
          servicesOptions: servicesOptions,
        });

        if (valid) {
          service = { ...service, ...validatedData };
        }

        resolve();
      }, 200);
    });
  }

  let adminDivisionChoices = [];

  function handleSubcategoriesChange(subcategories) {
    updateServicePresentation(
      servicesOptions.subcategories
        .filter((subcategory) => subcategories.includes(subcategory.value))
        .map((subcategory) => subcategory.label)
        .join(", ")
    );
  }

  function handleDiffusionZoneTypeChange(type) {
    if (type !== service.diffusionZoneType) {
      service.diffusionZoneType = type;
      service.diffusionZoneDetails = "";
      service.diffusionZoneDetailsDisplay = "";
      adminDivisionChoices = [];
    }
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

  setContext<ValidationContext>(contextValidationKey, {
    onBlur: handleEltChange,
    onChange: handleEltChange,
  });
</script>

<FieldSet noTopPadding title="Service de l'inclusion numérique">
  <div slot="help">
    <p class="text-f14">
      Le <b>Formulaire de l'inclusion numérique</b> est un outil de saisie
      compatible avec le
      <a
        href="https://lamednum.coop/schema-de-donnees-des-lieux-de-mediation-numerique-2/"
        target="_blank"
        rel="noreferrer"
        class="underline">schéma de données des lieux de médiation numérique</a
      >.
      <br />
      La standardisation des données de l'inclusion numérique permet de décrire l’offre
      disponible de manière harmonisée, assurant ainsi la compatibilité de ces données
      avec de nombreux outils.
    </p>
  </div>

  <FieldModel
    serviceValue={service.subcategories}
    options={servicesOptions.subcategories}
    type="array"
  >
    <SchemaField
      type="multiselect"
      label={serviceSchema.subcategories.name}
      schema={serviceSchema.subcategories}
      name="subcategories"
      errorMessages={$formErrors.subcategories}
      bind:value={service.subcategories}
      choices={subcategories}
      placeholder="Sélectionner"
      placeholderMulti="Sélectionner"
      onSelectChange={handleSubcategoriesChange}
    />
  </FieldModel>

  {#if concernedPublicOptions.length}
    <FieldModel
      serviceValue={service.concernedPublic}
      options={concernedPublicOptions}
      type="array"
    >
      <SchemaField
        type="multiselect"
        label={serviceSchema.concernedPublic.name}
        schema={serviceSchema.concernedPublic}
        name="concernedPublic"
        errorMessages={$formErrors.concernedPublic}
        bind:value={service.concernedPublic}
        choices={concernedPublicOptions}
        placeholder="Sélectionner"
        placeholderMulti="Sélectionner"
      />
    </FieldModel>
  {/if}

  {#if kindsOptions.length}
    <FieldModel
      serviceValue={service.kinds}
      options={kindsOptions}
      type="array"
    >
      <SchemaField
        type="checkboxes"
        label={serviceSchema.kinds.name}
        schema={serviceSchema.kinds}
        name="kinds"
        errorMessages={$formErrors.kinds}
        bind:value={service.kinds}
        choices={kindsOptions}
      />
    </FieldModel>
  {/if}

  <FieldModel serviceValue={service.feeCondition} type="text">
    <SelectField
      label="Frais à charge"
      name="feeCondition"
      placeholder="Choississez..."
      errorMessages={$formErrors.feeCondition}
      bind:value={service.feeCondition}
      choices={servicesOptions.feeConditions}
      display="vertical"
    />
  </FieldModel>

  {#if isNotFreeService(service.feeCondition)}
    <FieldModel serviceValue={service.feeDetails}>
      <SchemaField
        type="textarea"
        label="Détails des frais à charge"
        placeholder="Merci de détailler ici les frais à charge du bénéficiaire : adhésion, frais de location, frais de garde, etc., et les montants."
        schema={serviceSchema.feeDetails}
        name="feeDetails"
        errorMessages={$formErrors.feeDetails}
        bind:value={service.feeDetails}
      />
    </FieldModel>
  {/if}
</FieldSet>

<FieldSet title="Modalités">
  <div slot="help">
    <p class="text-f14">Modalités pour mobiliser le service.</p>
  </div>

  <FieldModel
    serviceValue={service.beneficiariesAccessModes}
    options={servicesOptions.beneficiariesAccessModes}
    type="array"
  >
    <SchemaField
      label={serviceSchema.beneficiariesAccessModes.name}
      type="checkboxes"
      choices={moveToTheEnd(
        servicesOptions.beneficiariesAccessModes,
        "value",
        "autre"
      )}
      schema={serviceSchema.coachOrientationModes}
      name="beneficiariesAccessModes"
      errorMessages={$formErrors.beneficiariesAccessModes}
      bind:value={service.beneficiariesAccessModes}
    />
  </FieldModel>

  {#if service.beneficiariesAccessModes.includes("autre")}
    <FieldModel serviceValue={service.beneficiariesAccessModesOther}>
      <SchemaField
        hideLabel
        placeholder="Merci de préciser la modalité"
        type="text"
        schema={serviceSchema.beneficiariesAccessModesOther}
        name="beneficiariesAccessModesOther"
        errorMessages={$formErrors.beneficiariesAccessModesOther}
        bind:value={service.beneficiariesAccessModesOther}
      />
    </FieldModel>
  {/if}
</FieldSet>

{#if !structure.latitude || !structure.longitude}
  <FieldSet title="Périmètre géographique d’intervention">
    <div slot="help">
      <p class="text-f14">
        Qu’il soit national, régional, départemental, intercommunal ou communal,
        le service peut être délimité aux bénéficiaires habitant sur un
        territoire spécifique.
      </p>

      <h5 class="mb-s0">QPV et ZRR</h5>
      <p class="text-f14">
        Activez cette option si votre offre s’adresse uniquement aux
        bénéficiaires résidants dans des Quartiers Prioritaires de la politique
        de la Ville ou des Zones de Revitalisation Rurale.
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
          handleChange={(details) => {
            service.diffusionZoneDetails = details;
          }}
          initialValue={service.diffusionZoneDetailsDisplay}
          bind:choices={adminDivisionChoices}
        />
      </SchemaField>
    {/if}
  </FieldSet>
{/if}

<FieldSet title="Accueil">
  <Button
    on:click={fillAddress}
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
