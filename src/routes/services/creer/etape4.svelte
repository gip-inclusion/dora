<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";

  import Field from "$lib/components/forms/field.svelte";

  import CustomLayout from "./_custom-layout.svelte";

  import NavButtons from "./_nav.svelte";
  let autoSuspend = false;
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $serviceOptions}
      <FieldSet title="Contact solution">
        <ModelField
          type="text"
          field={$serviceOptions.contactName}
          bind:value={$serviceCache.contactName} />
        <ModelField
          type="tel"
          field={$serviceOptions.contactPhone}
          bind:value={$serviceCache.contactPhone} />
        <ModelField
          type="email"
          field={$serviceOptions.contactEmail}
          bind:value={$serviceCache.contactEmail} />
        <ModelField
          type="url"
          field={$serviceOptions.contactUrl}
          bind:value={$serviceCache.contactUrl} />
        <ModelField
          type="toggle"
          field={$serviceOptions.isContactInfoPublic}
          bind:value={$serviceCache.isContactInfoPublic} />
      </FieldSet>

      <FieldSet title="Lieu">
        <ModelField
          type="checkboxes"
          field={$serviceOptions.locationKind}
          bind:value={$serviceCache.locationKind} />
        <ModelField
          type="url"
          field={$serviceOptions.remoteUrl}
          bind:value={$serviceCache.remoteUrl} />
        <ModelField
          type="text"
          field={$serviceOptions.address1}
          bind:value={$serviceCache.address1} />
        <ModelField
          type="text"
          field={$serviceOptions.address2}
          bind:value={$serviceCache.address2} />
        <ModelField
          type="text"
          field={$serviceOptions.postalCode}
          bind:value={$serviceCache.postalCode} />
        <ModelField
          type="text"
          field={$serviceOptions.city}
          bind:value={$serviceCache.city} />
        <ModelField
          type="hidden"
          field={$serviceOptions.cityCode}
          bind:value={$serviceCache.cityCode} />
        <ModelField
          type="hidden"
          field={$serviceOptions.longitude}
          bind:value={$serviceCache.longitude} />
        <ModelField
          type="hidden"
          field={$serviceOptions.latitude}
          bind:value={$serviceCache.latitude} />
      </FieldSet>

      <FieldSet title="Durée et modalités de disponibilité">
        <ModelField
          type="toggle"
          field={$serviceOptions.isTimeLimited}
          bind:value={$serviceCache.isTimeLimited} />
        <ModelField
          type="date"
          field={$serviceOptions.startDate}
          bind:value={$serviceCache.startDate} />
        <ModelField
          type="date"
          field={$serviceOptions.endDate}
          bind:value={$serviceCache.endDate} />
        <ModelField
          type="radios"
          field={$serviceOptions.recurrence}
          bind:value={$serviceCache.recurrence} />
        <ModelField
          type="text"
          field={$serviceOptions.recurrenceOther}
          bind:value={$serviceCache.recurrenceOther} />
        <Field
          type="toggle"
          label="Critères de suspension"
          bind:value={autoSuspend} />
        <ModelField
          type="number"
          minValue={1}
          field={$serviceOptions.suspensionCount}
          bind:value={$serviceCache.suspensionCount} />
        <ModelField
          type="date"
          field={$serviceOptions.suspensionDate}
          bind:value={$serviceCache.suspensionDate} />
      </FieldSet>
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="navbar">
    <NavButtons withBack withValidate backlink="etape3" />
  </svelte:fragment>
</CustomLayout>
