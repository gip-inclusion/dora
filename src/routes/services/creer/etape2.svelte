<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import CustomLayout from "./_custom-layout.svelte";
  import NavButtons from "./_nav.svelte";
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $serviceOptions}
      <FieldSet title="Conditions d'accès pour le bénéficiaire">
        <ModelField
          type="multiselect"
          placeholder="Choisissez ou ajoutez vos critères d’admission"
          field={$serviceOptions.accessConditions}
          bind:value={$serviceCache.accessConditions}
          bind:selectedItem={$serviceCache._accessConditionsItems} />
        <ModelField
          type="multiselect"
          placeholder="Sélectionnez ou ajoutez les publics que vous adressez"
          field={$serviceOptions.concernedPublic}
          bind:value={$serviceCache.concernedPublic}
          bind:selectedItem={$serviceCache._concernedPublicItems} />
        <ModelField
          type="toggle"
          field={$serviceOptions.isCumulative}
          bind:value={$serviceCache.isCumulative} />
        <ModelField
          type="toggle"
          field={$serviceOptions.hasFee}
          bind:value={$serviceCache.hasFee} />
        <ModelField
          type="text"
          hideLabel
          description="Merci de détailler les frais à charge et leurs éventuels critères de
      remboursement"
          field={$serviceOptions.feeDetails}
          bind:value={$serviceCache.feeDetails} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withBack withForward backlink="etape1" forwardlink="etape3" />
  </svelte:fragment>
</CustomLayout>
