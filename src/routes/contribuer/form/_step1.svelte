<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service-contrib.js";
  import StructureSearch from "$lib/components/structures/search.svelte";

  export let servicesOptions, service;
  export let establishment;

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

  function handleCityChange() {
    service.siret = "";
  }

  async function handleEstablishmentChange(newEstablishment) {
    service.siret = newEstablishment?.siret;
  }
</script>

<StructureSearch
  onEstablishmentChange={handleEstablishmentChange}
  onCityChange={handleCityChange}
  bind:establishment
/>

{#if service.siret}
  <FieldSet title="Présentez le service">
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
        Le nom de ce service, tel qu’il va être affiché dans les résultats de
        recherche et les fiches détail.
      </FieldHelp>
    </ModelField>

    <ModelField
      description="280 caractères maximum"
      placeholder="Décrivez brièvement ce service"
      type="textarea"
      label="Présentation résumée"
      schema={serviceSchema.shortDesc}
      name="shortDesc"
      errorMessages={$formErrors.shortDesc}
      bind:value={service.shortDesc}
    />

    <ModelField
      label="Descriptif complet du service"
      placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant ce service et ses spécificités."
      type="richtext"
      vertical
      schema={serviceSchema.fullDesc}
      name="fullDesc"
      errorMessages={$formErrors.fullDesc}
      bind:value={service.fullDesc}
      ><FieldHelp slot="helptext" title="Présentation résumée">
        <p>
          Contenu de présentation court qui apparait dans les résultats de
          recherche du site DORA. Résumez en une phrase les besoins auxquels ce
          service répond et apportez plus de détails dans la partie
          «&nbsp;Descriptif complet&nbsp;», si besoin est.
        </p>
        <p>
          <strong>Exemple de résumé :</strong> Faciliter vos déplacements en cas
          de reprise d'emploi ou de formation (entretien d'embauche, concours public...)
        </p>
      </FieldHelp></ModelField
    >
  </FieldSet>

  <FieldSet title="Typologie de service">
    <ModelField
      type="select"
      label="Thématique"
      schema={serviceSchema.category}
      bind:value={service.category}
      choices={servicesOptions.categories}
      name="category"
      errorMessages={$formErrors.category}
      onSelectChange={handleCategoryChange}
      placeholder="Choisissez la thématique principale"
      sortSelect
    >
      <FieldHelp slot="helptext" title="Catégorisation">
        Pour faciliter le référencement et la mise en avant de votre service, il
        est nécessaire de classer les services par thématiques et besoins
        auxquels ils répondent.
      </FieldHelp>
    </ModelField>

    <ModelField
      type="multiselect"
      label="Besoin(s) auxquels ce service répond"
      schema={serviceSchema.subcategories}
      name="subcategories"
      errorMessages={$formErrors.subcategories}
      bind:value={service.subcategories}
      choices={subcategories}
      placeholder="Choisissez les sous-catégories"
      placeholderMulti="Choisissez les sous-catégories"
      sortSelect
    />

    <ModelField
      type="checkboxes"
      label="Type de service"
      schema={serviceSchema.kinds}
      name="kinds"
      errorMessages={$formErrors.kinds}
      bind:value={service.kinds}
      choices={servicesOptions.kinds}
      description="Quelle est la nature de ce service."
    />
  </FieldSet>
{/if}
