<script>
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";

  import StructureForm from "../_structure_form.svelte";
  import SiretSearch from "./_siret_search.svelte";
  import CitySearch from "./_city_search.svelte";

  let selectedCity;
  let selectedEstablishment;
  let structure = {};

  let formErrors = {};

  function handleCityChange(city) {
    selectedCity = city;
    structure = {};
    selectedEstablishment = null;
    formErrors = {};
  }

  function handleEstablishmentChange(establishment) {
    selectedEstablishment = establishment;
    formErrors = {};
    structure = {};
    if (establishment) {
      structure.siret = establishment.siret;
      structure.name = establishment.name || establishment.parent;
      structure.address1 = establishment.addr1;
      structure.address2 = establishment.addr2;
      structure.city = (
        (establishment.city || "") +
        " " +
        (establishment.distrib || "")
      ).trim();
      structure.cityCode = establishment.citycode;
      structure.postalCode = establishment.postcode;
      structure.ape = establishment.ape;
      structure.longitude = establishment.longitude;
      structure.latitude = establishment.latitude;
    }
  }

  $: console.log(formErrors);
</script>

<FieldSet
  title="Retrouvez votre structure"
  description="On peut récuperer automatiquement les informations importantes de votre structure via la base SIRENE. Saissisez votre département et le numéro SIRET pour commencer.">
  <Field label="Commune" vertical>
    <CitySearch
      slot="input"
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
  <Field label="Le nom de votre structure ou le numéro SIRET" vertical>
    <SiretSearch
      slot="input"
      {selectedEstablishment}
      {selectedCity}
      disabled={!selectedCity?.value?.properties?.citycode}
      handleChange={handleEstablishmentChange}
      placeholder="Commencez à saisir et choisissez dans la liste" />
  </Field>
</FieldSet>

{#if structure.siret}
  <StructureForm {structure} formTitle="Présentez votre structure" />
{/if}
