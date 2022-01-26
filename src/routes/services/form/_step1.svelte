<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";

  import Info from "$lib/components/forms/form-info.svelte";

  export let servicesOptions, service, structures;
  let subcategories = [];

  function handleCategoryChange(category) {
    subcategories = category
      ? servicesOptions.subcategories.filter(({ value }) =>
          value.startsWith(category)
        )
      : [];

    service.subcategories = service.subcategories.filter((scat) =>
      scat.startsWith(category)
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
  <Info title="Périmètre de test">
    Dans un premier temps, seuls les services liés aux freins périphériques :
    <strong>mobilités</strong>, <strong>garde d'enfant</strong> et
    <strong>hébergement / logement</strong> sont testés.
  </Info>

  <ModelField
    type="select"
    label="Thématique"
    schema={serviceSchema.category}
    bind:value={service.category}
    choices={servicesOptions.categories}
    name="category"
    errorMessages={$formErrors.category}
    onSelectChange={handleCategoryChange}
    placeholder="Choisissez la catégorie principale"
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
    placeholder="Choisissez les sous-catégories"
    placeholderMulti="Choisissez les sous-catégories"
    sortSelect
  >
    <FieldHelp slot="helptext" title="Catégorisation">
      Pour permettre à nos utilisateurs de trouver facilement la solution que
      vous proposez, il est nécessaire de classer les services par catégorie.
    </FieldHelp>
  </ModelField>

  <ModelField
    type="checkboxes"
    label="Type de service"
    schema={serviceSchema.kinds}
    name="kinds"
    errorMessages={$formErrors.kinds}
    bind:value={service.kinds}
    choices={servicesOptions.kinds}
    description="Quel type de service proposez-vous ? "
  />
</FieldSet>

<FieldSet title="Présentez votre service">
  <ModelField
    label="Nom du service"
    type="text"
    placeholder="Ex. Aide aux frais liés à…"
    schema={serviceSchema.name}
    name="name"
    errorMessages={$formErrors.name}
    bind:value={service.name}
  />
  <ModelField
    description="280 caractères maximum"
    placeholder="Décrivez brièvement votre service"
    type="textarea"
    label="Résumé"
    schema={serviceSchema.shortDesc}
    name="shortDesc"
    errorMessages={$formErrors.shortDesc}
    bind:value={service.shortDesc}
  >
    <FieldHelp slot="helptext" title="Résumé">
      <p>
        Lors de l’affichage du service, nous aurons besoin de voir une
        présentation brève de ce que propose votre service avec seulement les
        éléments principaux.
      </p>
      <p>
        <strong>Par exemple :</strong>
        Faciliter vos déplacements en cas de recherche d'emploi (entretien d'embauche,
        concours public).
      </p>
    </FieldHelp>
  </ModelField>
  <ModelField
    label="Sessions & récurrence"
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
