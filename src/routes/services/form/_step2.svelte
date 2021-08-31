<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";

  export let servicesOptions;
  export let service;
</script>

<FieldSet title="Conditions d'accès pour le bénéficiaire">
  <ModelField
    type="multiselect"
    label="Critères d’accès"
    placeholder="Choisissez ou ajoutez vos critères d’admission"
    schema={serviceSchema.accessConditions}
    name="accessConditions"
    errorMessages={$formErrors.accessConditions}
    bind:value={service.accessConditions}
    choices={servicesOptions.accessConditions}>
    <FieldHelp slot="helptext" title="Critères">
      <p>
        <strong>Critères d’admission</strong><br />
        Précisez les critères d’éligibilité du public afin de recevoir des orientations
        adéquates
      </p>
      <p>
        <strong>Publics concernés</strong><br />Définissez bien les publics
        concernés, cela permettra d’orienter le bon public.
      </p>
      <p>
        <strong>Pré-requis ou compétences</strong><br />
        Quels sont les compétences, les diplômes qui limitent l’accès au service
        ?
      </p>
      <p>
        <strong>Service cumulable</strong><br />Ce service peut-il être cumulé à
        un autre ?
      </p>
    </FieldHelp></ModelField>

  <ModelField
    type="multiselect"
    label="Publics concernés"
    placeholder="Sélectionnez ou ajoutez les publics que vous adressez"
    schema={serviceSchema.concernedPublic}
    name="concernedPublic"
    errorMessages={$formErrors.concernedPublic}
    bind:value={service.concernedPublic}
    choices={servicesOptions.concernedPublic} />
  <ModelField
    type="multiselect"
    label="Quels sont les pré-requis ou compétences ?"
    placeholder="Choisissez ou ajoutez vos critères d’admission"
    schema={serviceSchema.requirements}
    name="requirements"
    errorMessages={$formErrors.requirements}
    bind:value={service.requirements}
    choices={servicesOptions.requirements} />
  <ModelField
    type="toggle"
    label="Service cumulable"
    schema={serviceSchema.isCumulative}
    name="isCumulative"
    errorMessages={$formErrors.isCumulative}
    bind:value={service.isCumulative} />
  <ModelField
    type="toggle"
    label="Frais à charge du bénéficiaire"
    schema={serviceSchema.hasFee}
    name="hasFee"
    errorMessages={$formErrors.hasFee}
    bind:value={service.hasFee} />

  <ModelField
    type="textarea"
    hideLabel
    placeholder="Merci de détailler les frais à charge et leurs éventuels critères de remboursement"
    visible={!!service.hasFee}
    schema={serviceSchema.feeDetails}
    name="feeDetails"
    errorMessages={$formErrors.feeDetails}
    bind:value={service.feeDetails} />
</FieldSet>
