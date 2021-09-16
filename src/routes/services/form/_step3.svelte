<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";

  export let servicesOptions, service;
  export let structures = undefined;
</script>

<FieldSet title="Modalités d'accès au service">
  <ModelField
    label="Comment le bénéficiaire peut accéder à ce service ?"
    type="checkboxes"
    choices={servicesOptions.beneficiariesAccessModes}
    schema={serviceSchema.beneficiariesAccessModes}
    name="beneficiariesAccessModes"
    errorMessages={$formErrors.beneficiariesAccessModes}
    bind:value={service.beneficiariesAccessModes}>
    <FieldHelp slot="helptext" title="Mobiliser le service">
      Quels sont les étapes à suivre pour pouvoir mobiliser le service ?
    </FieldHelp></ModelField>
  <ModelField
    visible={service.beneficiariesAccessModes.includes("OT")}
    hideLabel
    placeholder="Merci de préciser la modalité"
    type="text"
    schema={serviceSchema.beneficiariesAccessModesOther}
    name="beneficiariesAccessModesOther"
    errorMessages={$formErrors.beneficiariesAccessModesOther}
    bind:value={service.beneficiariesAccessModesOther} />
  <ModelField
    label="Comment orienter un bénéficiaire en tant qu’accompagnateur ?"
    type="checkboxes"
    choices={servicesOptions.coachOrientationModes}
    schema={serviceSchema.coachOrientationModes}
    name="coachOrientationModes"
    errorMessages={$formErrors.coachOrientationModes}
    bind:value={service.coachOrientationModes} />
  <ModelField
    visible={service.coachOrientationModes.includes("OT")}
    hideLabel
    placeholder="Merci de préciser la modalité"
    type="text"
    schema={serviceSchema.coachOrientationModesOther}
    name="coachOrientationModesOther"
    errorMessages={$formErrors.coachOrientationModesOther}
    bind:value={service.coachOrientationModesOther} />

  <ModelField
    label="Quels sont les justificatifs à fournir ?"
    placeholder="Sélectionnez les justificatifs à fournir"
    type="multiselect"
    schema={serviceSchema.credentials}
    name="credentials"
    errorMessages={$formErrors.credentials}
    bind:value={service.credentials}
    choices={servicesOptions.credentials}
    sortSelect />
  <Field
    type="custom"
    label="Partagez les documents à compléter"
    errorMessages={$formErrors.forms}>
    <FieldHelp slot="helptext" title="Justificatifs, documents">
      Mettre tous les documents maintenant, c’est permettre d’avoir des
      candidatures complètes avec moins d’aller/retour
    </FieldHelp>
    <Uploader
      slot="custom-input"
      structureSlug={service.structure}
      name="forms"
      on:blur
      bind:fileKeys={service.forms} />
  </Field>
  <ModelField
    label="Liens pratiques"
    placeholder="URL"
    type="url"
    schema={serviceSchema.onlineForm}
    name="onlineForm"
    errorMessages={$formErrors.onlineForm}
    bind:value={service.onlineForm} />
</FieldSet>
