<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import Uploader from "$lib/components/uploader.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";

  export let serviceOptions;
  export let service;
</script>

<FieldSet title="Modalités d'accès au service">
  <ModelField
    label="Comment mobiliser le service en tant que bénéficiaire ?"
    type="checkboxes"
    field={serviceOptions.beneficiariesAccessModes}
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
    field={serviceOptions.beneficiariesAccessModesOther}
    name="beneficiariesAccessModesOther"
    errorMessages={$formErrors.beneficiariesAccessModesOther}
    bind:value={service.beneficiariesAccessModesOther} />
  <ModelField
    label="Comment orienter un bénéficiaire en tant qu’accompagnateur ?"
    type="checkboxes"
    field={serviceOptions.coachOrientationModes}
    name="coachOrientationModes"
    errorMessages={$formErrors.coachOrientationModes}
    bind:value={service.coachOrientationModes} />
  <ModelField
    visible={service.coachOrientationModes.includes("OT")}
    hideLabel
    placeholder="Merci de préciser la modalité"
    type="text"
    field={serviceOptions.coachOrientationModesOther}
    name="coachOrientationModesOther"
    errorMessages={$formErrors.coachOrientationModesOther}
    bind:value={service.coachOrientationModesOther} />
  <ModelField
    placeholder="Choisissez ou ajoutez vos critères d’admission"
    type="multiselect"
    field={serviceOptions.requirements}
    name="requirements"
    errorMessages={$formErrors.requirements}
    bind:value={service.requirements}>
    <FieldHelp slot="helptext" title="Accès au service">
      Quels sont les compétences, les diplômes qui limitent l’accès au service ?
    </FieldHelp></ModelField>
  <ModelField
    placeholder="Sélectionnez les justificatifs à fournir"
    type="multiselect"
    field={serviceOptions.credentials}
    name="credentials"
    errorMessages={$formErrors.credentials}
    bind:value={service.credentials} />
  <Field
    type="custom"
    label={serviceOptions.forms.label}
    errorMessages={$formErrors.forms}>
    <FieldHelp slot="helptext" title="Justificatifs, documents">
      Mettre tous les documents maintenant, c’est permettre d’avoir des
      candidatures complètes avec moins d’aller/retour
    </FieldHelp>
    <Uploader
      slot="custom-input"
      folder={service.structure}
      name="forms"
      on:blur
      bind:fileKeys={service.forms} />
  </Field>
  <ModelField
    label="Le formulaire en ligne à compléter"
    placeholder="URL"
    type="url"
    field={serviceOptions.onlineForm}
    name="onlineForm"
    errorMessages={$formErrors.onlineForm}
    bind:value={service.onlineForm} />
</FieldSet>
