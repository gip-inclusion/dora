<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";
  import serviceSchema from "$lib/schemas/service.js";
  import AddableMultiselect from "$lib/components/forms/addable-multiselect.svelte";

  export let servicesOptions;
  export let service;
</script>

<FieldSet title="Conditions d'accès pour le bénéficiaire">
  <AddableMultiselect
    bind:values={service.accessConditions}
    structure={service.structure}
    choices={servicesOptions.accessConditions}
    errorMessages={$formErrors.accessConditions}
    name="accessConditions"
    label="Critères d’accès"
    placeholder="Aucun"
    placeholderMulti="Choisir un autre critères d’admission"
    schema={serviceSchema.accessConditions}
    sortSelect
  >
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
    </FieldHelp>
  </AddableMultiselect>

  <AddableMultiselect
    bind:values={service.concernedPublic}
    structure={service.structure}
    choices={servicesOptions.concernedPublic}
    errorMessages={$formErrors.concernedPublic}
    name="concernedPublic"
    label="Publics concernés"
    placeholder="Tous publics"
    placeholderMulti="Choisir un autre type de publics"
    schema={serviceSchema.concernedPublic}
    sortSelect
  />

  <AddableMultiselect
    bind:values={service.requirements}
    structure={service.structure}
    choices={servicesOptions.requirements}
    errorMessages={$formErrors.requirements}
    name="requirements"
    label="Quels sont les pré-requis ou compétences ?"
    placeholder="Aucun"
    placeholderMulti="Choisir un autre pré-requis"
    schema={serviceSchema.requirements}
    sortSelect
  />

  <ModelField
    type="toggle"
    label="Service cumulable"
    schema={serviceSchema.isCumulative}
    name="isCumulative"
    errorMessages={$formErrors.isCumulative}
    bind:value={service.isCumulative}
  />
  <ModelField
    type="toggle"
    label="Frais à charge du bénéficiaire"
    schema={serviceSchema.hasFee}
    name="hasFee"
    errorMessages={$formErrors.hasFee}
    bind:value={service.hasFee}
  />

  <ModelField
    type="textarea"
    hideLabel
    placeholder="Merci de détailler ici les frais à charge du bénéficiaire : adhésion, frais de location, frais de garde, etc., et les montants."
    visible={!!service.hasFee}
    schema={serviceSchema.feeDetails}
    name="feeDetails"
    errorMessages={$formErrors.feeDetails}
    bind:value={service.feeDetails}
  />
</FieldSet>
