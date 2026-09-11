<script lang="ts">
  import FieldSet from "$lib/components/display/fieldset.svelte";
  import type { Service, ServicesOptions } from "$lib/types";
  import AddressSearchSelect from "$lib/components/specialized/address-search-select.svelte";
  import FieldModel from "$lib/components/specialized/services/field-model.svelte";
  import FieldWrapper from "$lib/components/forms/field-wrapper.svelte";
  import {
    LOCATION_TYPE_BY_NAME,
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

  // les territoires déjà enregistrés ne figurent dans aucun résultat de
  // recherche : le back nous en fournit les libellés, reconstitués à partir des
  // seuls codes stockés
  const initialChoices = (service.zoneEligibiliteDisplay ?? []).map(
    ({ label, type, codes }) => ({
      label,
      value: serializeLocation({ type: LOCATION_TYPE_BY_NAME[type], codes }),
    })
  );

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
