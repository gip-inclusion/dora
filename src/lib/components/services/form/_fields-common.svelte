<script>
  import { setContext } from "svelte";

  import {
    formErrors,
    validate,
    contextValidationKey,
  } from "$lib/validation.js";
  import {
    moveToTheEnd,
    orderAndReformatSubcategories,
    arraysCompare,
  } from "$lib/utils";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import SchemaField from "$lib/components/forms/schema-field.svelte";
  import AddableMultiselect from "$lib/components/forms/addable-multiselect.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import FieldModel from "./_field-model.svelte";
  import SelectField from "$lib/components/form/select/select-field.svelte";
  import { isNotFreeService } from "$lib/utils/service";

  export let servicesOptions, serviceSchema, service, canAddChoices;
  export let model = null;
  export let typologyFieldDisabled = false;

  let subcategories = [];
  let showModelSubcategoriesUseValue = true;

  function handleCategoriesChange(categories) {
    subcategories = categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          categories.some((cat) => value.startsWith(cat))
        )
      : [];

    subcategories = orderAndReformatSubcategories(
      subcategories,
      categories,
      servicesOptions
    );

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );

    if (model) {
      showModelSubcategoriesUseValue = arraysCompare(
        categories,
        model.categories
      );
    }
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

  let showModel;

  $: showModel = !!service.model;

  let fullDesc;
  function useModelValue(propName) {
    return () => {
      service[propName] = model[propName];

      if (propName === "fullDesc") {
        fullDesc.updateValue(service.fullDesc);
      }
    };
  }
</script>

<FieldSet title="Présentation" {showModel}>
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
    type="markdown"
  >
    <SchemaField
      bind:this={fullDesc}
      label={serviceSchema.fullDesc.name}
      placeholder="Informations concernant le service et ses spécificités."
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
      sortSelect
      disabled={typologyFieldDisabled}
      readonly={typologyFieldDisabled}
    />
  </FieldModel>

  <FieldModel
    {showModel}
    value={model?.subcategories}
    serviceValue={service.subcategories}
    options={servicesOptions.subcategories}
    useValue={useModelValue("subcategories")}
    showUseValue={showModelSubcategoriesUseValue}
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
<FieldSet title="Publics" {showModel}>
  <div slot="help">
    <p class="text-f14">
      Publics auxquels le service s’adresse. Vous pouvez ajouter vos propres
      valeurs avec le bouton « Ajouter une autre option ». Si votre service est
      ouvert à tous, sans critères ou prérequis, laissez les champs avec les
      options par défaut.
    </p>
  </div>

  {#if servicesOptions.concernedPublic.length}
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
        canAdd={canAddChoices}
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.accessConditions.length}
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
        canAdd={canAddChoices}
      />
    </FieldModel>
  {/if}

  {#if servicesOptions.requirements.length}
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
        canAdd={canAddChoices}
      />
    </FieldModel>
  {/if}
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
    value={model?.feeCondition}
    serviceValue={service.feeCondition}
    useValue={useModelValue("feeCondition")}
    type="text"
  >
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
    <FieldModel
      {showModel}
      value={model?.feeDetails}
      serviceValue={service.feeDetails}
      useValue={useModelValue("feeDetails")}
    >
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

<FieldSet title="Documents" {showModel}>
  <div slot="help">
    <p class="text-f14">
      Justificatifs à fournir et documents à compléter pour postuler. Le lien
      redirige vers une page web qui présente le service (formulaire, fiche de
      prescription, simulateurs, etc.)
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

  {#if servicesOptions.credentials.length}
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
        canAdd={canAddChoices}
      />
    </FieldModel>
  {/if}

  <FieldModel
    {showModel}
    value={model?.onlineForm}
    serviceValue={service.onlineForm}
    useValue={useModelValue("onlineForm")}
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
