<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
</script>

{#if $serviceOptions}
  <h2 class="w-full mt-20 mb-4 text-xl font-bold ">
    Conditions d'accès pour le bénéficiaire
  </h2>

  <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-back2">
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
  </div>
  <NavButtons previousLink="etape1" nextLink="etape3" withValidate />
{/if}
