<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, "etape2", "etape4");
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
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
        bind:selectedItems={$serviceCache._requirementsItems} />
      <ModelField
        type="multiselect"
        field={$serviceOptions.credentials}
        bind:value={$serviceCache.credentials}
        bind:selectedItems={$serviceCache._credentialsItems} />
      <ModelField
        type="upload"
        field={$serviceOptions.forms}
        bind:value={$serviceCache.forms} />
      <ModelField
        type="multitext"
        field={$serviceOptions.onlineForms}
        bind:value={$serviceCache.onlineForms} />
    </FieldSet>
    <NavButtons withBack withForward />
  </form>
{/if}
