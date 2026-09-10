<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import AddressSearchSelect from "$lib/components/specialized/address-search-select.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import { getDepartment } from "$lib/utils/search-area";
  import {
    LocationType,
    parseLocation,
    serializeLocation,
  } from "$lib/utils/service-search-keyword";

  interface Props {
    servicesOptions: ServicesOptions;
    service: Service;
  }

  let { service = $bindable() }: Props = $props();

  let addressFieldValue = $state("");
  let addressSelectErrorMessage = $state("");

  // les départements déjà enregistrés ne figurent dans aucun résultat de
  // recherche : on fournit leurs libellés au Select pour qu’il puisse les afficher
  const initialChoices = (service.zoneEligibilite ?? [])
    .map((code) => getDepartment(code))
    .filter((department) => department !== null)
    .map((department) => ({
      label: `${department.label} (${department.code})`,
      value: serializeLocation({
        type: LocationType.Department,
        codes: [department.code],
      }),
    }));

  let selectedValues = $state(initialChoices.map((choice) => choice.value));

  // en sélection multiple, le Select transmet la totalité des valeurs
  // sélectionnées, et non la dernière ajoutée
  function handleAddressChange(newLocations: string[] | null) {
    if (newLocations?.length) {
      service.zoneEligibilite = [
        ...new Set(
          newLocations.flatMap((location) => parseLocation(location).codes)
        ),
      ];
    } else {
      addressFieldValue = "";
    }
  }
</script>

<FieldSet title="Périmètre d'éligibilité">
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
        bénéficiaires résidants dans des quartiers prioritaires de la politique
        de la ville (QPV) ou des zones France ruralités revitalisation (ZFRR).
      </p>
    </div>
  {/snippet}

  <FieldModel>
    <FieldWrapper
      id="zoneEligibilite"
      label="Secteurs éligibles"
      descriptionText="Par défaut au national. Précisez le ou les territoires concernés : départements, communes,…"
    >
      <AddressSearchSelect
        id="zoneEligibilite"
        placeholder="Saisissez un département, une commune…"
        multiple
        bind:addressFieldValue
        {handleAddressChange}
        {addressSelectErrorMessage}
        bind:value={selectedValues}
        initialLabels={initialChoices}
        extraClass="w-full"
      />
    </FieldWrapper>
  </FieldModel>
</FieldSet>
