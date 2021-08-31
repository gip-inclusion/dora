<script context="module">
  import { getStructuresOptions } from "$lib/structures";

  export async function load({ _page, _fetch, _session, _context }) {
    return { props: { structuresOptions: await getStructuresOptions() } };
  }
</script>

<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";
  import CitySearch from "$lib/components/forms/city-search.svelte";

  import StructureFormWrapper from "../_structure-form-wrapper.svelte";
  import SiretSearch from "./_siret_search.svelte";
  import { siretWasAlreadyClaimed } from "$lib/structures";
  import structureSchema from "$lib/schemas/structure.js";

  import { alertIcon } from "$lib/icons.js";

  export let structuresOptions;

  let selectedCity;
  let selectedEstablishment;

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
    selectedEstablishment = null;
  }

  async function establishmentAlreadyCreated(siret) {
    const result = await siretWasAlreadyClaimed(siret);
    if (result.ok) {
      return result.result;
    }
    return false;
  }

  async function handleEstablishmentChange(establishment) {
    selectedEstablishment = establishment;
    alreadyClaimedEstablishment = null;
    structure = JSON.parse(JSON.stringify(defaultStructure));
    if (establishment) {
      alreadyClaimedEstablishment = await establishmentAlreadyCreated(
        establishment.siret
      );
      if (!alreadyClaimedEstablishment) {
        structure.siret = establishment.siret;
        structure.name = establishment.name || establishment.parent;
        structure.address1 = establishment.addr1;
        structure.address2 = establishment.addr2;
        structure.city = `${establishment.city || ""} ${
          establishment.distrib || ""
        }`.trim();
        structure.cityCode = establishment.citycode;
        structure.postalCode = establishment.postcode;
        structure.ape = establishment.ape;
        structure.longitude = establishment.longitude;
        structure.latitude = establishment.latitude;
      }
    }
  }
</script>

<FieldSet
  title="Retrouvez votre structure"
  description="On peut récuperer automatiquement les informations importantes de votre structure via la base SIRENE. Saissisez votre département et le numéro SIRET pour commencer.">
  <Field type="custom" label="Commune" vertical>
    <CitySearch
      slot="custom-input"
      name="city-select"
      placeholder="Saisissez le nom de votre ville"
      handleChange={handleCityChange} />
    <FieldHelp title="Récupération des données existantes" slot="helptext">
      <p>
        Pour faciliter l’étape de saisie, nous récupérons pour vous des données
        que l’État possède déjà. Une série d’éléments complémentaires vous
        seront demandés afin de réaliser et promouvoir un profil complet de
        votre structure. Pensez à mettre à jour régulièrement ces informations.
      </p>
    </FieldHelp>
  </Field>
  <Field
    type="custom"
    label="Le nom de votre structure ou le numéro SIRET"
    vertical>
    <SiretSearch
      slot="custom-input"
      name="siret-select"
      {selectedCity}
      disabled={!selectedCity?.properties?.citycode}
      handleChange={handleEstablishmentChange}
      placeholder="Commencez à saisir et choisissez dans la liste" />
  </Field>
</FieldSet>

{#if alreadyClaimedEstablishment}
  <div
    class="text-error text-xl flex flex-row items-center justify-center pt-1/2 mt-2">
    <div class="w-3 h-3 mr-1 fill-current ">
      {@html alertIcon}
    </div>
    <p>
      Cette structure a déjà été saisie dans DORA. Vous pouvez la
      <a
        class="underline"
        href="/structures/{alreadyClaimedEstablishment?.slug}">
        visualiser</a
      >.
    </p>
  </div>
{/if}

<StructureFormWrapper
  {structure}
  {structuresOptions}
  formTitle="Présentez votre structure"
  visible={structure.siret} />
