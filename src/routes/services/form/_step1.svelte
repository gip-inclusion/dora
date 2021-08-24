<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";

  import Info from "./_info.svelte";

  export let serviceOptions;
  export let service;
</script>

<FieldSet title="">
  <ModelField
    type="select"
    field={serviceOptions.structure}
    name="structure"
    errorMessages={$formErrors.structure}
    bind:value={service.structure}
    placeholder="Sélectionnez votre structure" />
</FieldSet>

<FieldSet title="Typologie de service">
  <Info title="Périmètre de test">
    Pour tester rapidement un maximum de leviers et itérer rapidement, l’équipe
    va se focaliser sur un périmètre d’expérimentation réduit en matière
    d’offre. Thématiques d’offres ciblées : <strong
      >mobilité, <strong>garde d’enfant</strong> et
      <strong>hébergement/logement</strong>.
    </strong></Info>

  <ModelField
    type="multiselect"
    field={serviceOptions.categories}
    name="categories"
    errorMessages={$formErrors.categories}
    bind:value={service.categories}
    placeholder="Choisissez la catégorie principale" />
  <ModelField
    type="multiselect"
    field={serviceOptions.subcategories}
    name="subcategories"
    errorMessages={$formErrors.subcategories}
    bind:value={service.subcategories}
    placeholder="Choisissez les sous-catégories">
    <FieldHelp slot="helptext" title="Catégorisation">
      Pour permettre à nos utilisateurs de trouver facilement la solution que
      vous proposez. Il est nécessaire de classer les offres par catégorie et de
      préciser le type d’offre.
    </FieldHelp>
  </ModelField>

  <ModelField
    type="checkboxes"
    field={serviceOptions.kinds}
    name="kinds"
    errorMessages={$formErrors.kinds}
    bind:value={service.kinds}
    description="Quel type de service proposez-vous ? " />

  <ModelField
    type="toggle"
    label="Droit commun"
    field={serviceOptions.isCommonLaw}
    name="isCommonLaw"
    errorMessages={$formErrors.isCommonLaw}
    bind:value={service.isCommonLaw}
    description="Il s’agit d’un service de Droit commun - mobilisé équitablement sur l’ensemble du territoire ?" />
</FieldSet>

<FieldSet title="Présentez votre service">
  <ModelField
    label="Nom de l’offre"
    type="text"
    placeholder="Ex. Aide aux frais liés à…"
    field={serviceOptions.name}
    name="name"
    errorMessages={$formErrors.name}
    bind:value={service.name} />
  <ModelField
    description="280 caractères maximum"
    placeholder="Décrivez brièvement votre service"
    type="textarea"
    field={serviceOptions.shortDesc}
    name="shortDesc"
    errorMessages={$formErrors.shortDesc}
    bind:value={service.shortDesc}>
    <FieldHelp slot="helptext" title="Résumé">
      <p>
        Lors de l’affichage du service, nous aurons besoin de voir une
        présentation brève de ce que propose votre service avec seulement les
        éléments principaux.
      </p>
      <p>
        <strong>Par exemple :</strong>
        <em
          >Faciliter vos déplacements en cas de recherche d'emploi (entretien
          d'embauche, concours public).</em>
      </p>
    </FieldHelp>
  </ModelField>
  <ModelField
    label="Descriptif complet du service"
    placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre service et ses spécificités."
    type="richtext"
    vertical
    field={serviceOptions.fullDesc}
    name="fullDesc"
    errorMessages={$formErrors.fullDesc}
    bind:value={service.fullDesc} />
</FieldSet>
