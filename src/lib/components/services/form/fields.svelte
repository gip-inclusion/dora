<script>
  import { tick, setContext, onMount } from "svelte";

  import { getModel, getServicesOptions } from "$lib/services";
  import { getStructure } from "$lib/structures";
  import {
    formErrors,
    validate,
    contextValidationKey,
  } from "$lib/validation.js";
  import schema, { fields, fieldsRequired } from "$lib/schemas/service.js";
  import { moveToTheEnd } from "$lib/utils";

  import CenteredGrid from "$lib/components/layout/centered-grid.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";
  import AddableMultiselect from "$lib/components/forms/addable-multiselect.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";
  import AddressSearch from "$lib/components/forms/street-search.svelte";
  import AdminDivisionSearch from "$lib/components/forms/admin-division-search.svelte";
  import Button from "$lib/components/button.svelte";
  import { formatSchema } from "$lib/schemas/utils";
  import FieldModel from "./field-model.svelte";

  export let servicesOptions, service, structures, structure;
  export let isModel = false;
  export let model = null;
  let subcategories = [];
  const propsWithSpecificFields = [
    "accessConditions",
    "concernedPublic",
    "requirements",
    "credentials",
  ];

  function handleCategoriesChange(categories) {
    subcategories = categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          categories.some((cat) => value.startsWith(cat))
        )
      : [];

    subcategories = moveToTheEnd(subcategories, "label", "Autre", true);

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }

  // met à jour les options de service et le modèle en fonction des champs spécifiques
  function updateServiceOptions() {
    propsWithSpecificFields.forEach((propName) => {
      // options de services qui appartiennent à la structure courante
      const structureServicesOptions = servicesOptions[propName].filter(
        (o) =>
          !o.structure || (structure?.slug && o.structure === structure.slug)
      );

      if (!isModel && service.model && model) {
        // si ce champs spécifique existe dans les options de service
        // -> on modifie le modèle avec l'id du champs spécifique
        // sinon (le champs spécifique n'existe pas dans les options de service)
        // -> on l'ajoute dans les options de service
        model[propName].forEach((value, i) => {
          // si le type est une string, c'est un champs spécifique
          if (typeof value === "string") {
            const option = structureServicesOptions.find(
              (o) => o.label === value
            );

            if (option) {
              model[propName][i] = option.value;
            } else {
              servicesOptions[propName] = [
                ...servicesOptions[propName],
                { value, label: value, structure: structure.slug },
              ];
            }
          }
        });
      }

      // sur le service,
      // suprimme les champs spécifiques qui n'aapartiennent pas à la structure
      if (structure) {
        const structureOptionsValues = servicesOptions[propName]
          .filter((c) => !c.structure || c.structure === structure.slug)
          .map((c) => c.value);

        service[propName] = service[propName].filter((value) =>
          structureOptionsValues.includes(value)
        );
      }
    });
  }

  async function handleStructureChange(slug) {
    if (slug) {
      structure = await getStructure(slug);
      servicesOptions = await getServicesOptions();
      service.structure = slug;
      if (!isModel && service.model) {
        model = await getModel(model.slug);
      }
      updateServiceOptions();
    }
  }

  // Il s'agit d'une édition de service existant
  const showStructures = service.structure ? false : structures.length > 1;

  export let adminDivisionChoices = [];

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

  const serviceSchema = formatSchema(
    schema,
    fields[isModel ? "model" : "service"],
    fieldsRequired[isModel ? "model" : "service"]
  );

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

  let showModel = !!model;

  async function unsync() {
    service.model = null;
    showModel = false;
  }

  function useModelValue(propName) {
    return () => {
      service[propName] = model[propName];
    };
  }

  onMount(() => {
    updateServiceOptions();
  });
</script>

<CenteredGrid bgColor="bg-gray-bg">
  <div class="lg:w-2/3">
    <FieldSet noTopPadding>
      <SchemaField
        type="select"
        schema={serviceSchema.structure}
        label={serviceSchema.structure.name}
        choices={structures.map((s) => ({ value: s.slug, label: s.name }))}
        name="structure"
        errorMessages={$formErrors.structure}
        bind:value={service.structure}
        onSelectChange={handleStructureChange}
        sortSelect
        placeholder="Sélectionner"
        disabled={!showStructures}
      />
    </FieldSet>
  </div>
</CenteredGrid>

<hr />
<CenteredGrid bgColor={service.model ? "bg-info-light" : "bg-gray-bg"}>
  {#if service.model}
    <div class="lg:flex lg:items-center lg:justify-between">
      <h3>Synchronisé avec un modèle</h3>
      <Button label="Détacher du modèle" secondary small on:click={unsync} />
    </div>
  {/if}

  <div class={showModel ? "" : "lg:w-2/3"}>
    <FieldSet title="Présentation" {showModel} noTopPadding={!service.model}>
      <div slot="help">
        <p class="text-f14">
          Le <b>Résumé</b> présente le service en une phrase courte. Il apparait
          dans les résultats de recherche.
        </p>
        <p class="text-f14">
          <strong>Exemple</strong> :
          <i>
            Faciliter vos déplacements en cas de reprise d’emploi ou de
            formation (entretien d’embauche, concours public…)
          </i>
        </p>
        <p class="text-f14">
          Si besoin, détaillez dans la partie
          <b>Description</b>.
        </p>
      </div>

      <FieldModel
        {showModel}
        value={model?.name}
        serviceValue={service.name}
        useValue={useModelValue("name")}
      >
        <SchemaField
          label={serviceSchema.name.name}
          type="text"
          placeholder="Compléter"
          schema={serviceSchema.name}
          name="name"
          errorMessages={$formErrors.name}
          bind:value={service.name}
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.shortDesc}
        serviceValue={service.shortDesc}
        useValue={useModelValue("shortDesc")}
      >
        <SchemaField
          description="280 caractères maximum"
          placeholder="Compléter"
          type="textarea"
          label={serviceSchema.shortDesc.name}
          schema={serviceSchema.shortDesc}
          name="shortDesc"
          errorMessages={$formErrors.shortDesc}
          bind:value={service.shortDesc}
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.fullDesc}
        serviceValue={service.fullDesc}
        useValue={useModelValue("fullDesc")}
        paddingTop
        type="html"
      >
        <SchemaField
          label={serviceSchema.fullDesc.name}
          placeholder="Informations concernants le service et ses spécificités."
          type="richtext"
          vertical
          schema={serviceSchema.fullDesc}
          name="fullDesc"
          errorMessages={$formErrors.fullDesc}
          bind:value={service.fullDesc}
        />
      </FieldModel>
    </FieldSet>

    <FieldSet title="Typologie" {showModel}>
      <div slot="help">
        <p class="text-f14">
          Classez le service par thématiques et besoins pour faciliter son
          référencement.
        </p>
      </div>

      <FieldModel
        {showModel}
        value={model?.categories}
        serviceValue={service.categories}
        options={servicesOptions.categories}
        useValue={useModelValue("categories")}
        type="array"
      >
        <SchemaField
          type="multiselect"
          label={serviceSchema.categories.name}
          schema={serviceSchema.categories}
          bind:value={service.categories}
          choices={servicesOptions.categories}
          name="categories"
          errorMessages={$formErrors.categories}
          onSelectChange={handleCategoriesChange}
          placeholderMulti="Sélectionner"
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.subcategories}
        serviceValue={service.subcategories}
        options={servicesOptions.subcategories}
        useValue={useModelValue("subcategories")}
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
          sortSelect
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.kinds}
        serviceValue={service.kinds}
        options={servicesOptions.kinds}
        useValue={useModelValue("kinds")}
        type="array"
      >
        <SchemaField
          type="checkboxes"
          label={serviceSchema.kinds.name}
          schema={serviceSchema.kinds}
          name="kinds"
          errorMessages={$formErrors.kinds}
          bind:value={service.kinds}
          choices={servicesOptions.kinds}
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.isCumulative}
        serviceValue={service.isCumulative}
        useValue={useModelValue("isCumulative")}
        type="boolean"
      >
        <SchemaField
          type="toggle"
          label={serviceSchema.isCumulative.name}
          schema={serviceSchema.isCumulative}
          name="isCumulative"
          errorMessages={$formErrors.isCumulative}
          bind:value={service.isCumulative}
          description="Cumulable avec d’autres services"
        />
      </FieldModel>
    </FieldSet>

    {#if service.structure}
      <FieldSet title="Publics" {showModel}>
        <div slot="help">
          <p class="text-f14">
            Publics auxquels le service s’adresse. Vous pouvez ajouter vos
            propres valeurs avec le bouton « Ajouter une autre option ». Si
            votre service est ouvert à tous, sans critères ou prérequis, laissez
            les champs avec les options par défaut.
          </p>
        </div>

        <FieldModel
          {showModel}
          value={model?.concernedPublic}
          serviceValue={service.concernedPublic}
          options={servicesOptions.concernedPublic}
          useValue={useModelValue("concernedPublic")}
          type="array"
        >
          <AddableMultiselect
            bind:values={service.concernedPublic}
            structure={service.structure}
            choices={servicesOptions.concernedPublic}
            errorMessages={$formErrors.concernedPublic}
            name="concernedPublic"
            label={serviceSchema.concernedPublic.name}
            placeholder="Tous publics"
            placeholderMulti="Sélectionner"
            schema={serviceSchema.concernedPublic}
            sortSelect
            description="Plusieurs choix possibles"
          />
        </FieldModel>

        <FieldModel
          {showModel}
          value={model?.accessConditions}
          serviceValue={service.accessConditions}
          options={servicesOptions.accessConditions}
          useValue={useModelValue("accessConditions")}
          type="array"
        >
          <AddableMultiselect
            bind:values={service.accessConditions}
            structure={service.structure}
            choices={servicesOptions.accessConditions}
            errorMessages={$formErrors.accessConditions}
            name="accessConditions"
            label={serviceSchema.accessConditions.name}
            placeholder="Aucun"
            placeholderMulti="Choisir un autre critères d’admission"
            schema={serviceSchema.accessConditions}
            sortSelect
            description="Plusieurs choix possibles"
          />
        </FieldModel>

        <FieldModel
          {showModel}
          value={model?.requirements}
          serviceValue={service.requirements}
          options={servicesOptions.requirements}
          useValue={useModelValue("requirements")}
          type="array"
        >
          <AddableMultiselect
            bind:values={service.requirements}
            structure={service.structure}
            choices={servicesOptions.requirements}
            errorMessages={$formErrors.requirements}
            name="requirements"
            label={serviceSchema.requirements.name}
            placeholder="Aucun"
            placeholderMulti="Choisir un autre pré-requis"
            schema={serviceSchema.requirements}
            sortSelect
            description="Plusieurs choix possibles"
          />
        </FieldModel>
      </FieldSet>

      <FieldSet title="Modalités" {showModel}>
        <div slot="help">
          <p class="text-f14">Modalités pour mobiliser le service.</p>
        </div>

        <FieldModel
          {showModel}
          value={model?.coachOrientationModes}
          serviceValue={service.coachOrientationModes}
          options={servicesOptions.coachOrientationModes}
          useValue={useModelValue("coachOrientationModes")}
          type="array"
        >
          <SchemaField
            label={serviceSchema.coachOrientationModes.name}
            type="checkboxes"
            choices={moveToTheEnd(
              servicesOptions.coachOrientationModes,
              "value",
              "autre"
            )}
            schema={serviceSchema.coachOrientationModes}
            name="coachOrientationModes"
            errorMessages={$formErrors.coachOrientationModes}
            bind:value={service.coachOrientationModes}
          />
        </FieldModel>

        {#if service.coachOrientationModes.includes("autre")}
          <FieldModel
            {showModel}
            value={model?.coachOrientationModesOther}
            serviceValue={service.coachOrientationModesOther}
            useValue={useModelValue("coachOrientationModesOther")}
          >
            <SchemaField
              hideLabel
              placeholder="Compléter"
              type="text"
              schema={serviceSchema.coachOrientationModesOther}
              name="coachOrientationModesOther"
              errorMessages={$formErrors.coachOrientationModesOther}
              bind:value={service.coachOrientationModesOther}
            />
          </FieldModel>
        {/if}

        <FieldModel
          {showModel}
          value={model?.beneficiariesAccessModes}
          serviceValue={service.beneficiariesAccessModes}
          options={servicesOptions.beneficiariesAccessModes}
          useValue={useModelValue("beneficiariesAccessModes")}
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
            schema={serviceSchema.beneficiariesAccessModes}
            name="beneficiariesAccessModes"
            errorMessages={$formErrors.beneficiariesAccessModes}
            bind:value={service.beneficiariesAccessModes}
          />
        </FieldModel>

        {#if service.beneficiariesAccessModes.includes("autre")}
          <FieldModel
            {showModel}
            value={model?.beneficiariesAccessModesOther}
            serviceValue={service.beneficiariesAccessModesOther}
            useValue={useModelValue("beneficiariesAccessModesOther")}
          >
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

        <FieldModel
          {showModel}
          value={model?.hasFee}
          serviceValue={service.hasFee}
          useValue={useModelValue("hasFee")}
          type="boolean"
        >
          <SchemaField
            type="toggle"
            label={serviceSchema.hasFee.name}
            schema={serviceSchema.hasFee}
            name="hasFee"
            errorMessages={$formErrors.hasFee}
            bind:value={service.hasFee}
          />
        </FieldModel>

        {#if !!service.hasFee}
          <FieldModel
            {showModel}
            value={model?.feeDetails}
            serviceValue={service.feeDetails}
            useValue={useModelValue("feeDetails")}
          >
            <SchemaField
              type="textarea"
              hideLabel
              placeholder="Adhésion, frais de location, frais de garde, etc., et les montants."
              schema={serviceSchema.feeDetails}
              name="feeDetails"
              errorMessages={$formErrors.feeDetails}
              bind:value={service.feeDetails}
            />
          </FieldModel>
        {/if}
      </FieldSet>

      <FieldSet title="Documents" {showModel}>
        <div slot="help">
          <p class="text-f14">
            Justificatifs à fournir et documents à compléter pour postuler. Le
            lien redirige vers une page web qui présente le service (formulaire,
            fiche de prescription, simulateurs, etc.)
          </p>
        </div>
        <FieldModel
          {showModel}
          value={model?.forms}
          serviceValue={service.forms}
          useValue={useModelValue("forms")}
          type="files"
        >
          <Field
            type="custom"
            label={serviceSchema.forms.name}
            errorMessages={$formErrors.forms}
          >
            <Uploader
              slot="custom-input"
              structureSlug={service.structure}
              name="forms"
              on:blur
              bind:fileKeys={service.forms}
            />
          </Field>
        </FieldModel>

        <FieldModel
          {showModel}
          value={model?.credentials}
          serviceValue={service.credentials}
          useValue={useModelValue("credentials")}
          options={servicesOptions.credentials}
          type="array"
        >
          <AddableMultiselect
            bind:values={service.credentials}
            structure={service.structure}
            choices={servicesOptions.credentials}
            errorMessages={$formErrors.credentials}
            name="credentials"
            label={serviceSchema.credentials.name}
            placeholder="Aucun"
            placeholderMulti="Choisir un autre justificatif"
            schema={serviceSchema.credentials}
            sortSelect
          />
        </FieldModel>

        <FieldModel
          {showModel}
          value={model?.onlineForm}
          serviceValue={service.onlineForm}
          useValue={useModelValue("forms")}
        >
          <SchemaField
            label={serviceSchema.onlineForm.name}
            placeholder="URL"
            type="url"
            schema={serviceSchema.onlineForm}
            name="onlineForm"
            errorMessages={$formErrors.onlineForm}
            bind:value={service.onlineForm}
          />
        </FieldModel>
      </FieldSet>
    {/if}

    <FieldSet title="Périodicité" {showModel}>
      <div slot="help">
        <p class="text-f14">
          La durée limitée permet de supendre automatiquement la visibilité du
          service dans les résultat de recherche.
        </p>
      </div>
      <FieldModel
        {showModel}
        value={model?.recurrence}
        serviceValue={service.recurrence}
        useValue={useModelValue("recurrence")}
      >
        <SchemaField
          label={serviceSchema.recurrence.name}
          type="text"
          placeholder="Ex. Tous les jours à 14h, une fois par mois, etc."
          schema={serviceSchema.recurrence}
          name="recurrence"
          errorMessages={$formErrors.recurrence}
          bind:value={service.recurrence}
        />
      </FieldModel>

      <FieldModel
        {showModel}
        value={model?.suspensionDate}
        serviceValue={service.suspensionDate}
        useValue={useModelValue("suspensionDate")}
      >
        <SchemaField
          label={serviceSchema.suspensionDate.name}
          type="date"
          schema={serviceSchema.suspensionDate}
          name="suspensionDate"
          errorMessages={$formErrors.suspensionDate}
          bind:value={service.suspensionDate}
        />
      </FieldModel>
    </FieldSet>
  </div>
</CenteredGrid>

{#if !isModel}
  <hr />

  <CenteredGrid bgColor="bg-gray-bg">
    <div class="lg:w-2/3">
      <FieldSet title="Zone de diffusion" noTopPadding>
        <div slot="help">
          <p class="text-f14">
            Si le service est reservé aux habitants d'un territoire.
          </p>

          <h5 class="mb-s0">QPV et ZRR</h5>
          <p class="text-f14">
            Activez cette option si votre offre s’adresse uniquement aux
            bénéficiaires résidants dans des Quartiers Prioritaires de la
            politique de la Ville ou des Zones de Revitalisation Rurale.
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

      <FieldSet title="Lieu">
        <SchemaField
          type="checkboxes"
          label={serviceSchema.locationKinds.name}
          schema={serviceSchema.locationKinds}
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
            label={serviceSchema.remoteUrl.name}
            schema={serviceSchema.remoteUrl}
            name="remoteUrl"
            errorMessages={$formErrors.remoteUrl}
            bind:value={service.remoteUrl}
          />
        {/if}

        {#if structure && service.locationKinds.includes("en-presentiel")}
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
            Coordonnées de la personne responsable de la réception et du
            traitement des demandes d’orientation. À défaut, renseignez le
            courriel et le numéro de téléphone de votre structure.
          </p>
          <p class="text-f14">
            Par défaut, ces informations sont disponibles uniquement aux
            accompagnateurs qui ont un compte DORA. En cochant la case « Rendre
            public », les informations seront rendues disponibles à tous les
            visiteurs du site.
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
    </div>
  </CenteredGrid>
{/if}
