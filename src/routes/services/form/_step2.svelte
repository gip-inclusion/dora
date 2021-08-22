<script>
  import { serviceCache } from "./_stores.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import { formErrors } from "$lib/validation.js";

  export let serviceOptions;
</script>

<FieldSet title="Conditions d'accès pour le bénéficiaire">
  <ModelField
    type="multiselect"
    label="Critères d’accès"
    placeholder="Choisissez ou ajoutez vos critères d’admission"
    field={serviceOptions.accessConditions}
    name="accessConditions"
    errorMessages={$formErrors.accessConditions}
    bind:value={$serviceCache.accessConditions}>
    <FieldHelp slot="helptext" title="Critères">
      <p>
        <strong>Critères d’admission</strong>
        <br /> Précisez les critères d’éligibilité du public afin de recevoir des
        orientations adéquates
      </p>
      <p>
        <strong>Publics concernés</strong><br />Définissez bien les publics
        concernés, cela permettra d’orienter le bon public.
      </p>
      <p>
        <strong>Service cumulable</strong>
        <br />Ce service peut-il être cumulé à un autre ?
      </p>
    </FieldHelp></ModelField>

  <ModelField
    type="multiselect"
    placeholder="Sélectionnez ou ajoutez les publics que vous adressez"
    field={serviceOptions.concernedPublic}
    name="concernedPublic"
    errorMessages={$formErrors.concernedPublic}
    bind:value={$serviceCache.concernedPublic} />
  <ModelField
    type="toggle"
    field={serviceOptions.isCumulative}
    name="isCumulative"
    errorMessages={$formErrors.isCumulative}
    bind:value={$serviceCache.isCumulative} />
  <ModelField
    type="toggle"
    field={serviceOptions.hasFee}
    name="hasFee"
    errorMessages={$formErrors.hasFee}
    bind:value={$serviceCache.hasFee} />

  <ModelField
    type="text"
    hideLabel
    placeholder="Merci de détailler les frais à charge et leurs éventuels critères de
      remboursement"
    visible={!!$serviceCache.hasFee}
    field={serviceOptions.feeDetails}
    name="feeDetails"
    errorMessages={$formErrors.feeDetails}
    bind:value={$serviceCache.feeDetails} />
</FieldSet>
