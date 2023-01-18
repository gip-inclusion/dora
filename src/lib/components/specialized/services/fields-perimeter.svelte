<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AdminDivisionSearchField from "$lib/components/inputs/admin-division-search-field.svelte";
  import SelectField from "$lib/components/inputs/select-field.svelte";
  import ToggleField from "$lib/components/inputs/toggle-field.svelte";
  import type { Schema } from "$lib/validation/schemas/utils";

  export let schema: Schema;
  export let servicesOptions, service;
  let adminDivisionChoices = [];

  function handleDiffusionZoneTypeChange(type) {
    if (type !== service.diffusionZoneType) {
      service.diffusionZoneType = type;
      service.diffusionZoneDetails = "";
      service.diffusionZoneDetailsDisplay = "";
      adminDivisionChoices = [];
    }
  }

  function handlediffusionZoneDetailsChange(details) {
    service.diffusionZoneDetails = details;
  }
</script>

<FieldSet title="Périmètre géographique d’intervention">
  <div slot="help">
    <p class="text-f14">
      Qu’il soit national, régional, départemental, intercommunal ou communal,
      le service peut être délimité aux bénéficiaires habitant sur un territoire
      spécifique.
    </p>

    <h5 class="mb-s0">QPV et ZRR</h5>
    <p class="text-f14">
      Activez cette option si votre offre s’adresse uniquement aux bénéficiaires
      résidants dans des Quartiers Prioritaires de la politique de la Ville ou
      des Zones de Revitalisation Rurale.
    </p>
  </div>

  <SelectField
    id="diffusionZoneType"
    schema={schema.diffusionZoneType}
    choices={servicesOptions.diffusionZoneType}
    onChange={handleDiffusionZoneTypeChange}
    initialValue={service.diffusionZoneTypeDisplay}
  />

  {#if service.diffusionZoneType !== "country"}
    <AdminDivisionSearchField
      id="diffusionZoneDetails"
      schema={schema.diffusionZoneDetails}
      description="Commencez à saisir le nom et choisissez dans la liste."
      searchType={service.diffusionZoneType}
      onChange={handlediffusionZoneDetailsChange}
      initialValue={service.diffusionZoneDetailsDisplay}
      bind:choices={adminDivisionChoices}
    />
  {/if}

  <ToggleField
    id="qpvOrZrr"
    schema={schema.qpvOrZrr}
    bind:value={service.qpvOrZrr}
  />
</FieldSet>
