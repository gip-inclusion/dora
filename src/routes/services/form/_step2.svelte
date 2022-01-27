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
    description="Précisez les critères d’éligibilité du public afin de recevoir des orientations adéquates. Plusieurs choix possibles."
  >
    <FieldHelp slot="helptext" title="Critères">
      <p>
        <strong>Critères d’éligibilité</strong><br />
        Définissez le type de publics auxquels votre service s’adresse. Si parmi
        les choix proposés pour les « critères d’accès », pour les « publics concernés »
        ou pour « les prérequis ou compétences » vous pouvez ajouter vos propres
        critères grâce au bouton « Ajouter une autre option ». Si votre service est
        ouvert à tout le monde, sans critères ou prérequis, laissez les champs avec
        les options par défaut.
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
    description="Ces critères permettent d’orienter le bon public vers votre service. Plusieurs choix possibles."
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
    description="Plusieurs choix possibles."
  />

  <ModelField
    type="toggle"
    label="Service cumulable"
    schema={serviceSchema.isCumulative}
    name="isCumulative"
    errorMessages={$formErrors.isCumulative}
    bind:value={service.isCumulative}
    description="Votre service est cumulable avec d’autres services ? "
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
