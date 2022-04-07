<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";

  export let servicesOptions, service, structures;
  let subcategories = [];

  function handleCategoryChange(categories) {
    subcategories = categories.length
      ? servicesOptions.subcategories.filter(({ value }) =>
          categories.some((cat) => value.startsWith(cat))
        )
      : [];

    service.subcategories = service.subcategories.filter((scat) =>
      categories.some((cat) => scat.startsWith(cat))
    );
  }

  function cleanOptions(field, structure) {
    const flatChoices = servicesOptions[field]
      .filter((c) => c.structure == null || c.structure === structure)
      .map((c) => c.value);
    service[field] = service[field].filter((value) =>
      flatChoices.includes(value)
    );
  }

  function handleStructureChange(structure) {
    cleanOptions("accessConditions", structure);
    cleanOptions("concernedPublic", structure);
    cleanOptions("requirements", structure);
    cleanOptions("credentials", structure);
  }
</script>

{#if structures.length > 1}
  <FieldSet title="">
    <ModelField
      type="select"
      schema={serviceSchema.structure}
      label="Structure"
      choices={structures.map((s) => ({ value: s.slug, label: s.name }))}
      name="structure"
      errorMessages={$formErrors.structure}
      bind:value={service.structure}
      onSelectChange={handleStructureChange}
      sortSelect
      placeholder="Sélectionnez votre structure"
    />
  </FieldSet>
{/if}

<FieldSet title="Typologie de service">
  <ModelField
    type="multiselect"
    label="Thématiques"
    schema={serviceSchema.categories}
    bind:value={service.categories}
    choices={servicesOptions.categories}
    name="categories"
    errorMessages={$formErrors.categories}
    onSelectChange={handleCategoryChange}
    placeholder="Choisissez la thématique principale"
    sortSelect
  />
  <ModelField
    type="multiselect"
    label="Besoin(s)"
    schema={serviceSchema.subcategories}
    name="subcategories"
    errorMessages={$formErrors.subcategories}
    bind:value={service.subcategories}
    choices={subcategories}
    placeholder="Choisissez le besoin correspondant"
    placeholderMulti="Choisissez les besoins correspondants"
    sortSelect
    description="Besoin(s) auxquels votre service répond."
  >
    <FieldHelp slot="helptext" title="Catégorisation">
      Pour faciliter le référencement et la mise en avant de votre service, il
      est nécessaire de classer les services par thématiques et besoins auxquels
      ils répondent.
    </FieldHelp>
  </ModelField>

  <ModelField
    type="checkboxes"
    label="Type"
    schema={serviceSchema.kinds}
    name="kinds"
    errorMessages={$formErrors.kinds}
    bind:value={service.kinds}
    choices={servicesOptions.kinds}
    description="Quelle est la nature de votre service."
  />
</FieldSet>

<FieldSet title="Présentez votre service">
  <ModelField
    label="Titre du service"
    type="text"
    placeholder="Ex. Aide aux frais liés à…"
    schema={serviceSchema.name}
    name="name"
    errorMessages={$formErrors.name}
    bind:value={service.name}
  >
    <FieldHelp slot="helptext" title="Titre du service">
      Le nom de votre service, tel qu’il va être affiché dans les résultats de
      recherche et les fiches détail.
    </FieldHelp>
  </ModelField>
  <ModelField
    description="280 caractères maximum"
    placeholder="Décrivez brièvement votre service"
    type="textarea"
    label="Présentation résumée"
    schema={serviceSchema.shortDesc}
    name="shortDesc"
    errorMessages={$formErrors.shortDesc}
    bind:value={service.shortDesc}
  >
    <FieldHelp slot="helptext" title="Résumé">
      <p>
        Contenu de présentation court qui apparait dans les résultats de
        recherche du site DORA. Résumez en une phrase les besoins auxquels votre
        service répond et apportez plus de détails dans la partie « Descriptif
        complet », si besoin est.
      </p>
      <p>
        <strong>Exemple de résumé</strong> : Faciliter vos déplacements en cas de
        reprise d'emploi ou de formation (entretien d'embauche, concours public...)
      </p>
    </FieldHelp>
  </ModelField>
  <ModelField
    label="Sessions et récurrence"
    description="À quelle fréquence votre service est-il disponible ?"
    type="text"
    placeholder="Ex. Tous les jours, une fois par mois, etc."
    schema={serviceSchema.recurrence}
    name="recurrence"
    errorMessages={$formErrors.recurrence}
    bind:value={service.recurrence}
  />
  <ModelField
    label="Descriptif complet du service"
    placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre service et ses spécificités."
    type="richtext"
    vertical
    schema={serviceSchema.fullDesc}
    name="fullDesc"
    errorMessages={$formErrors.fullDesc}
    bind:value={service.fullDesc}
  />
</FieldSet>
