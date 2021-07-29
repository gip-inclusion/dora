<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  function handleSubmit(evt) {
    persistAndGo(evt, "etape2", "etape4");
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">
      Modalités d'accès au service
    </h2>

    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-gray-01">
      <Field
        type="checkboxes"
        field={$serviceOptions.beneficiariesAccessModes}
        bind:value={$service.beneficiariesAccessModes} />

      <Field
        type="text"
        field={$serviceOptions.beneficiariesAccessModesOther}
        bind:value={$service.beneficiariesAccessModesOther} />

      <Field
        type="checkboxes"
        field={$serviceOptions.coachOrientationModes}
        bind:value={$service.coachOrientationModes} />
      <Field
        type="text"
        field={$serviceOptions.coachOrientationModesOther}
        bind:value={$service.coachOrientationModesOther} />
      <Field
        type="multiselect"
        field={$serviceOptions.requirements}
        bind:value={$service.requirements}
        bind:selectedItems={$service._requirementsItems} />
      <Field
        type="multiselect"
        field={$serviceOptions.credentials}
        bind:value={$service.credentials}
        bind:selectedItems={$service._credentialsItems} />

      <Field
        type="upload"
        field={$serviceOptions.forms}
        bind:value={$service.forms} />

      <Field
        type="multitext"
        field={$serviceOptions.onlineForms}
        bind:value={$service.onlineForms} />
    </div>
    <NavButtons withBack withForward />
  </form>
{/if}
