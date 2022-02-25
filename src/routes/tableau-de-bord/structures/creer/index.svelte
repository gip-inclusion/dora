<script context="module">
  import { getStructuresOptions } from "$lib/structures";

  export async function load() {
    return { props: { structuresOptions: await getStructuresOptions() } };
  }
</script>

<script>
  import StructureFormWrapper from "$lib/components/structures/form-wrapper.svelte";
  import StructureSearch from "$lib/components/structures/search.svelte";
  import { siretWasAlreadyClaimed } from "$lib/structures";
  import structureSchema from "$lib/schemas/structure.js";

  import { alertIcon } from "$lib/icons.js";

  export let structuresOptions;

  let selectedCity;

  const defaultStructure = Object.fromEntries(
    Object.entries(structureSchema).map(([fieldName, props]) => [
      fieldName,
      props.default,
    ])
  );
  let structure = JSON.parse(JSON.stringify(defaultStructure));

  let alreadyClaimedEstablishment;

  function handleCityChange(city) {
    selectedCity = city;
    structure = JSON.parse(JSON.stringify(defaultStructure));
  }

  async function establishmentAlreadyCreated(siret) {
    const result = await siretWasAlreadyClaimed(siret);
    if (result.ok) {
      return result.result;
    }
    return false;
  }

  async function handleEstablishmentChange(establishment) {
    alreadyClaimedEstablishment = null;
    structure = JSON.parse(JSON.stringify(defaultStructure));
    if (establishment) {
      alreadyClaimedEstablishment = await establishmentAlreadyCreated(
        establishment.siret
      );
      if (!alreadyClaimedEstablishment) {
        structure.siret = establishment.siret;
        structure.name = establishment.name;
        structure.address1 = establishment.address1;
        structure.address2 = establishment.address2;
        structure.city = establishment.city;
        structure.cityCode = establishment.cityCode;
        structure.postalCode = establishment.postalCode;
        structure.ape = establishment.ape;
        structure.longitude = establishment.longitude;
        structure.latitude = establishment.latitude;
      }
    }
  }
</script>

<svelte:head>
  <title>Créer une structure | DORA</title>
</svelte:head>

<StructureSearch
  onEstablishmentChange={handleEstablishmentChange}
  onCityChange={handleCityChange}
/>

{#if alreadyClaimedEstablishment}
  <div
    class="mt-s16 flex flex-row items-center justify-center pt-s4 text-f18 text-error"
  >
    <div class="mr-s8 h-s24 w-s24 fill-current">
      {@html alertIcon}
    </div>
    <p>
      Cette structure a déjà été saisie dans DORA. Vous pouvez la
      <a
        class="underline"
        href="/tableau-de-bord/structures/{alreadyClaimedEstablishment?.slug}"
      >
        visualiser
      </a>.
    </p>
  </div>
{/if}

<StructureFormWrapper
  {structure}
  {structuresOptions}
  formTitle="Présentez votre structure"
  visible={structure.siret}
/>
