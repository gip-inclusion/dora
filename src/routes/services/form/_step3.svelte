<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";
  import AddableMultiselect from "$lib/components/forms/addable-multiselect.svelte";

  export let servicesOptions, service;
</script>

<FieldSet title="Modalités d'accès au service">
  <ModelField
    label="Comment un bénéficiaire peut accéder à ce service ?"
    type="checkboxes"
    choices={servicesOptions.beneficiariesAccessModes}
    schema={serviceSchema.beneficiariesAccessModes}
    name="beneficiariesAccessModes"
    errorMessages={$formErrors.beneficiariesAccessModes}
    bind:value={service.beneficiariesAccessModes}
  >
    <FieldHelp slot="helptext" title="Comment mobiliser ce service">
      Quelles sont les modalités à suivre pour pouvoir mobiliser votre service ?
    </FieldHelp></ModelField
  >
  <ModelField
    visible={service.beneficiariesAccessModes.includes("OT")}
    hideLabel
    placeholder="Merci de préciser la modalité"
    type="text"
    schema={serviceSchema.beneficiariesAccessModesOther}
    name="beneficiariesAccessModesOther"
    errorMessages={$formErrors.beneficiariesAccessModesOther}
    bind:value={service.beneficiariesAccessModesOther}
  />
  <ModelField
    label="Comment orienter un bénéficiaire en tant qu’accompagnateur ?"
    type="checkboxes"
    choices={servicesOptions.coachOrientationModes}
    schema={serviceSchema.coachOrientationModes}
    name="coachOrientationModes"
    errorMessages={$formErrors.coachOrientationModes}
    bind:value={service.coachOrientationModes}
  />
  <ModelField
    visible={service.coachOrientationModes.includes("OT")}
    hideLabel
    placeholder="Merci de préciser la modalité"
    type="text"
    schema={serviceSchema.coachOrientationModesOther}
    name="coachOrientationModesOther"
    errorMessages={$formErrors.coachOrientationModesOther}
    bind:value={service.coachOrientationModesOther}
  />

  <AddableMultiselect
    bind:values={service.credentials}
    structure={service.structure}
    choices={servicesOptions.credentials}
    errorMessages={$formErrors.credentials}
    name="credentials"
    label="Quels sont les justificatifs à fournir ?"
    placeholder="Aucun"
    placeholderMulti="Choisir un autre justificatif"
    schema={serviceSchema.credentials}
    sortSelect
  />

  <Field
    type="custom"
    label="Partagez les documents à compléter"
    errorMessages={$formErrors.forms}
  >
    <FieldHelp slot="helptext" title="Documents requis">
      Listez les justificatifs à fournir et mettez à disposition les documents à
      compléter afin de recevoir des candidatures complètes, avec moins
      d’aller-retour. Utilisez la section liens pratiques pour rediriger vers
      plus d’informations concernant la mobilisation de votre service
      (formulaire, fiche de prescription, simulateurs, etc.)..
    </FieldHelp>
    <Uploader
      slot="custom-input"
      structureSlug={service.structure}
      name="forms"
      on:blur
      bind:fileKeys={service.forms}
    />
  </Field>
  <ModelField
    label="Liens pratiques"
    placeholder="URL que vous souhaitez mettre en avant"
    type="url"
    schema={serviceSchema.onlineForm}
    name="onlineForm"
    errorMessages={$formErrors.onlineForm}
    bind:value={service.onlineForm}
  />
</FieldSet>
