<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, "etape1", "etape3");
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
    <FieldSet title="Conditions d'accès pour le bénéficiaire">
      <Field
        type="multiselect"
        placeholder="Choisissez ou ajoutez vos critères d’admission"
        field={$serviceOptions.accessConditions}
        bind:value={$service.accessConditions}
        bind:selectedItems={$service._accessConditionsItems} />
      <Field
        type="multiselect"
        placeholder="Sélectionnez ou ajoutez les publics que vous adressez"
        field={$serviceOptions.concernedPublic}
        bind:value={$service.concernedPublic}
        bind:selectedItems={$service._concernedPublicItems} />
      <Field
        type="toggle"
        field={$serviceOptions.isCumulative}
        bind:value={$service.isCumulative} />
      <Field
        type="toggle"
        field={$serviceOptions.hasFee}
        bind:value={$service.hasFee} />
      <Field
        type="text"
        noLabel
        description="Merci de détailler les frais à charge et leurs éventuels critères de
      remboursement"
        field={$serviceOptions.feeDetails}
        bind:value={$service.feeDetails} />
    </FieldSet>
    <NavButtons withBack withForward />
  </form>
{/if}
