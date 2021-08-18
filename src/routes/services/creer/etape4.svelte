<script>
  import { serviceCache, serviceOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import ModelField from "$lib/components/forms/model-field.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import { formErrors } from "$lib/validation.js";

  import CustomLayout from "./_custom-layout.svelte";

  let autoSuspend = false;
</script>

<CustomLayout>
  {#if $serviceOptions}
    <FieldSet title="Contact référent">
      <ModelField
        label="Nom du contact"
        placeholder="Prénom et nom"
        type="text"
        field={$serviceOptions.contactName}
        name="contactName"
        errorMessage={$formErrors.contactName}
        bind:value={$serviceCache.contactName}>
        <FieldHelp slot="helptext" title="Contact référent">
          Merci de préciser les coordonnées de la personne en charge de ce
          service.
        </FieldHelp></ModelField>
      <ModelField
        type="tel"
        placeholder="05 ou 06 00 00 00 00"
        field={$serviceOptions.contactPhone}
        name="contactPhone"
        errorMessage={$formErrors.contactPhone}
        bind:value={$serviceCache.contactPhone} />
      <ModelField
        type="email"
        placeholder="Votre adresse e-mail"
        field={$serviceOptions.contactEmail}
        name="contactEmail"
        errorMessage={$formErrors.contactEmail}
        bind:value={$serviceCache.contactEmail} />
      <ModelField
        label="Rendre les informations publiques"
        type="toggle"
        field={$serviceOptions.isContactInfoPublic}
        name="isContactInfoPublic"
        errorMessage={$formErrors.isContactInfoPublic}
        bind:value={$serviceCache.isContactInfoPublic} />
    </FieldSet>

    <FieldSet title="Lieu">
      <ModelField
        type="checkboxes"
        field={$serviceOptions.locationKind}
        name="locationKind"
        errorMessage={$formErrors.locationKind}
        bind:value={$serviceCache.locationKind}>
        <FieldHelp slot="helptext" title="Lieu de déroulement">
          Merci de préciser si le service ou l’accompagnement se déroule en
          présentiel ou bien à distance. Si c’est à distance, merci de préciser
          le lien de la visioconférence.
        </FieldHelp></ModelField>
      <ModelField
        placeholder="https://"
        type="url"
        visible={$serviceCache.locationKind.includes("RE")}
        field={$serviceOptions.remoteUrl}
        name="remoteUrl"
        errorMessage={$formErrors.remoteUrl}
        bind:value={$serviceCache.remoteUrl} />
      <ModelField
        type="text"
        placeholder="Saisissez et validez votre ville"
        field={$serviceOptions.city}
        name="city"
        errorMessage={$formErrors.city}
        bind:value={$serviceCache.city} />
      <ModelField
        type="text"
        placeholder="Saisissez et validez votre adresse"
        field={$serviceOptions.address1}
        name="address1"
        errorMessage={$formErrors.address1}
        bind:value={$serviceCache.address1} />
      <ModelField
        type="text"
        placeholder="Compléments d’adresse"
        field={$serviceOptions.address2}
        name="address2"
        errorMessage={$formErrors.address2}
        bind:value={$serviceCache.address2} />
      <ModelField
        type="text"
        placeholder="Code postal"
        field={$serviceOptions.postalCode}
        name="postalCode"
        errorMessage={$formErrors.postalCode}
        bind:value={$serviceCache.postalCode} />
      <ModelField
        type="hidden"
        field={$serviceOptions.cityCode}
        name="cityCode"
        errorMessage={$formErrors.cityCode}
        bind:value={$serviceCache.cityCode} />
      <ModelField
        type="hidden"
        field={$serviceOptions.longitude}
        name="longitude"
        errorMessage={$formErrors.longitude}
        bind:value={$serviceCache.longitude} />
      <ModelField
        type="hidden"
        field={$serviceOptions.latitude}
        name="latitude"
        errorMessage={$formErrors.latitude}
        bind:value={$serviceCache.latitude} />
    </FieldSet>

    <FieldSet title="Durée et modalités de disponibilité">
      <ModelField
        label="Votre service est limité dans le temps ?"
        type="toggle"
        field={$serviceOptions.isTimeLimited}
        name="isTimeLimited"
        errorMessage={$formErrors.isTimeLimited}
        bind:value={$serviceCache.isTimeLimited} />
      <ModelField
        type="date"
        field={$serviceOptions.startDate}
        name="startDate"
        errorMessage={$formErrors.startDate}
        visible={!!$serviceCache.isTimeLimited}
        bind:value={$serviceCache.startDate}>
        <FieldHelp slot="helptext" title="Suspension">
          En configurant la suspension de votre service (avec une limite de
          temps ou de candidatures), vous pouvez mieux gérer la visibilité de
          votre service et sa mise à jour.
        </FieldHelp></ModelField>
      <ModelField
        type="date"
        visible={!!$serviceCache.isTimeLimited}
        field={$serviceOptions.endDate}
        name="endDate"
        errorMessage={$formErrors.endDate}
        bind:value={$serviceCache.endDate} />
      <ModelField
        type="radios"
        field={$serviceOptions.recurrence}
        name="recurrence"
        errorMessage={$formErrors.recurrence}
        bind:value={$serviceCache.recurrence} />
      <ModelField
        type="text"
        placeholder="Préciser"
        hideLabel
        visible={$serviceCache.recurrence === "OT"}
        field={$serviceOptions.recurrenceOther}
        name="recurrenceOther"
        errorMessage={$formErrors.recurrenceOther}
        bind:value={$serviceCache.recurrenceOther} />
      <Field
        name="autoSuspend"
        type="toggle"
        label="Critères de suspension"
        bind:value={autoSuspend} />
      <ModelField
        label="Oui, à partir d’un nombre d’inscriptions :"
        placeholder="Préciser le nombre maximum"
        visible={autoSuspend}
        type="number"
        minValue={1}
        field={$serviceOptions.suspensionCount}
        name="suspensionCount"
        errorMessage={$formErrors.suspensionCount}
        bind:value={$serviceCache.suspensionCount} />
      <ModelField
        label="Oui, à partir d’une date :"
        type="date"
        visible={autoSuspend}
        field={$serviceOptions.suspensionDate}
        name="suspensionDate"
        errorMessage={$formErrors.suspensionDate}
        bind:value={$serviceCache.suspensionDate} />
    </FieldSet>
  {/if}
</CustomLayout>
