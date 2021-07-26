<script>
  import { service } from "./_creation-store.js";
  import { serviceOptions } from "./_services-store.js";

  import Field from "$lib/components/forms/field.svelte";

  import NavButtons from "./_nav-buttons.svelte";
  import { persistAndGo } from "./_nav.js";

  const autoSuspendField = {
    value: false,
    label: "Critères de suspension",
  };

  function handleSubmit(evt) {
    persistAndGo(evt, "etape3", null);
  }
</script>

{#if $serviceOptions}
  <form on:submit|preventDefault={handleSubmit}>
    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">Contact solution</h2>
    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-back2">
      <Field
        type="text"
        field={$serviceOptions.contactName}
        bind:value={$service.contactName} />

      <Field
        type="tel"
        field={$serviceOptions.contactPhone}
        bind:value={$service.contactPhone} />
      <Field
        type="email"
        field={$serviceOptions.contactEmail}
        bind:value={$service.contactEmail} />
      <Field
        type="url"
        field={$serviceOptions.contactUrl}
        bind:value={$service.contactUrl} />
      <Field
        type="toggle"
        field={$serviceOptions.isContactInfoPublic}
        bind:value={$service.isContactInfoPublic} />
    </div>
    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">Lieu</h2>
    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-back2">
      <Field
        type="checkboxes"
        field={$serviceOptions.locationKind}
        bind:value={$service.locationKind} />

      <Field
        type="url"
        field={$serviceOptions.remoteUrl}
        bind:value={$service.remoteUrl} />
      <Field
        type="text"
        field={$serviceOptions.address1}
        bind:value={$service.address1} />
      <Field
        type="text"
        field={$serviceOptions.address2}
        bind:value={$service.address2} />

      <Field
        type="text"
        field={$serviceOptions.postalCode}
        bind:value={$service.postalCode} />

      <Field
        type="text"
        field={$serviceOptions.city}
        bind:value={$service.city} />

      <Field
        type="hidden"
        field={$serviceOptions.cityCode}
        bind:value={$service.cityCode} />

      <Field
        type="hidden"
        field={$serviceOptions.longitude}
        bind:value={$service.longitude} />

      <Field
        type="hidden"
        field={$serviceOptions.latitude}
        bind:value={$service.latitude} />
    </div>

    <h2 class="w-full mt-20 mb-4 text-xl font-bold ">
      Durée et modalités de disponibilité
    </h2>

    <div class="flex flex-col max-w-xl gap-6 p-8 mx-auto mt-8 bg-back2">
      <Field
        type="toggle"
        field={$serviceOptions.isTimeLimited}
        bind:value={$service.isTimeLimited} />

      <Field
        type="date"
        field={$serviceOptions.startDate}
        bind:value={$service.startDate} />
      <Field
        type="date"
        field={$serviceOptions.endDate}
        bind:value={$service.endDate} />
      <Field
        type="radios"
        field={$serviceOptions.recurrence}
        bind:value={$service.recurrence} />
      <Field
        type="text"
        field={$serviceOptions.recurrenceOther}
        bind:value={$service.recurrenceOther} />
      <Field
        type="toggle"
        field={autoSuspendField}
        bind:value={$service._autoSuspendField} />
      <Field
        type="number"
        min={1}
        field={$serviceOptions.suspensionCount}
        bind:value={$service.suspensionCount} />
      <Field
        type="date"
        field={$serviceOptions.suspensionDate}
        bind:value={$service.suspensionDate} />
    </div>
    <NavButtons withBack withValidate />
  </form>
{/if}
