<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import CustomLayout from "./_custom-layout.svelte";

  import NavButtons from "./_nav.svelte";

  $: console.log($serviceCache);
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $serviceOptions}
      <FieldSet title="Modalités d'accès au service">
        <ModelField
          type="checkboxes"
          field={$serviceOptions.beneficiariesAccessModes}
          bind:value={$serviceCache.beneficiariesAccessModes} />
        <ModelField
          type="text"
          field={$serviceOptions.beneficiariesAccessModesOther}
          bind:value={$serviceCache.beneficiariesAccessModesOther} />
        <ModelField
          type="checkboxes"
          field={$serviceOptions.coachOrientationModes}
          bind:value={$serviceCache.coachOrientationModes} />
        <ModelField
          type="text"
          field={$serviceOptions.coachOrientationModesOther}
          bind:value={$serviceCache.coachOrientationModesOther} />
        <ModelField
          type="multiselect"
          field={$serviceOptions.requirements}
          bind:value={$serviceCache.requirements}
          bind:selectedItem={$serviceCache._requirementsItems} />
        <ModelField
          type="multiselect"
          field={$serviceOptions.credentials}
          bind:value={$serviceCache.credentials}
          bind:selectedItem={$serviceCache._credentialsItems} />
        <ModelField
          type="files"
          field={$serviceOptions.forms}
          bind:value={$serviceCache.forms} />
        <ModelField
          type="multitext"
          field={$serviceOptions.onlineForms}
          bind:value={$serviceCache.onlineForms} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withBack withForward backlink="etape2" forwardlink="etape4" />
  </svelte:fragment>
</CustomLayout>
