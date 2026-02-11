<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import AdminDivisionSearchField from "$lib/components/forms/fields/admin-division-search-field.svelte";
  import BooleanRadioButtonsField from "$lib/components/forms/fields/boolean-radio-buttons-field.svelte";
  import SelectField from "$lib/components/forms/fields/select-field.svelte";
  import type { GeoApiValue, Service, ServicesOptions } from "$lib/types";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
  }

  let { servicesOptions, service = $bindable() }: Props = $props();
  let adminDivisionChoices = $state([]);

  function handleDiffusionZoneTypeChange(type) {
    if (type !== service.diffusionZoneType) {
      service.diffusionZoneType = type;
      service.diffusionZoneDetails = "";
      service.diffusionZoneDetailsDisplay = "";
      adminDivisionChoices = [];
    }
  }

  function handlediffusionZoneDetailsChange(details: GeoApiValue) {
    service.diffusionZoneDetails = details?.code;
  }
</script>

<FieldSet title="Périmètre géographique d’intervention">
  {#snippet help()}
    <div>
      <p class="text-f14">
        Qu’il soit national, régional, départemental, intercommunal ou communal,
        le service peut être délimité aux bénéficiaires habitant sur un
        territoire spécifique.
      </p>

      <h5 class="mb-s0">QPV et ZFRR</h5>
      <p class="text-f14">
        Activez cette option si votre offre s’adresse uniquement aux
        bénéficiaires résidants dans des Quartiers Prioritaires de la politique
        de la Ville ou des Zones Françaises de Revitalisation Rurale.
      </p>
    </div>
  {/snippet}

  <SelectField
    id="diffusionZoneType"
    choices={servicesOptions.diffusionZoneType}
    onChange={handleDiffusionZoneTypeChange}
    initialValue={service.diffusionZoneTypeDisplay}
    description="Térritoire déterminant l’éligibilité des bénéficiaires."
  />

  {#if service.diffusionZoneType !== "country"}
    <AdminDivisionSearchField
      id="diffusionZoneDetails"
      description="Commencez à saisir le nom et choisissez dans la liste."
      searchType={service.diffusionZoneType}
      onChange={handlediffusionZoneDetailsChange}
      initialValue={service.diffusionZoneDetailsDisplay}
      bind:choices={adminDivisionChoices}
    />
  {/if}

  <BooleanRadioButtonsField
    id="qpvOrZrr"
    bind:value={service.qpvOrZrr}
    description="Le service est destiné aux Quartiers prioritaire de la politique de la ville ou aux Zones françaises de revitalisation rurale."
  />
</FieldSet>
