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
    errorMessage={$formErrors.accessConditions}
    bind:value={$serviceCache.accessConditions}
    bind:selectedItem={$serviceCache._accessConditionsItems}>
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
    errorMessage={$formErrors.concernedPublic}
    bind:value={$serviceCache.concernedPublic}
    bind:selectedItem={$serviceCache._concernedPublicItems} />
  <ModelField
    type="toggle"
    field={serviceOptions.isCumulative}
    name="isCumulative"
    errorMessage={$formErrors.isCumulative}
    bind:value={$serviceCache.isCumulative} />
  <ModelField
    type="toggle"
    field={serviceOptions.hasFee}
    name="hasFee"
    errorMessage={$formErrors.hasFee}
    bind:value={$serviceCache.hasFee} />

  <ModelField
    type="text"
    hideLabel
    placeholder="Merci de détailler les frais à charge et leurs éventuels critères de
      remboursement"
    visible={!!$serviceCache.hasFee}
    field={serviceOptions.feeDetails}
    name="feeDetails"
    errorMessage={$formErrors.feeDetails}
    bind:value={$serviceCache.feeDetails} />
</FieldSet>
