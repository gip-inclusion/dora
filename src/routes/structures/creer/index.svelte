<script>
  import { structureOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";

  import ModelField from "$lib/components/forms/model-field.svelte";

  import ValidateButton from "./_validate.svelte";

  import SiretSearch from "./_siret_search.svelte";
  import CitySearch from "./_city_search.svelte";

  let selectedCity;
  let selectedEstablishment;
  let structure = {};

  function handleCityChange(city) {
    selectedCity = city;
    structure = {};
    selectedEstablishment = null;
  }

  function handleEstablishmentChange(establishment) {
    selectedEstablishment = establishment;
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
</script>

{#if $structureOptions}
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
          Pour faciliter l’étape de saisie, nous récupérons pour vous des
          données que l’État possède déjà. Une série d’éléments complémentaires
          vous seront demandés afin de réaliser et promouvoir un profil complet
          de votre structure. Pensez à mettre à jour régulièrement ces
          informations.
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
    <FieldSet title="Présentez votre Structure">
      <ModelField
        type="text"
        label="SIRET"
        field={$structureOptions.siret}
        disabled
        bind:value={structure.siret}
        vertical>
        <FieldHelp title="Completez les informations" slot="helptext">
          <p>
            Vérifiez l’exactitude des informations récupérées et complétez les
            autres.
          </p>
        </FieldHelp></ModelField>
      <ModelField
        type="text"
        label="Nom de la structure"
        field={$structureOptions.name}
        bind:value={structure.name}
        vertical />
      <ModelField
        type="select"
        label="Typologie de la structure"
        placeholder="choisissez"
        field={$structureOptions.typology}
        bind:value={structure.typology}
        vertical />
      <ModelField
        type="text"
        label="Adresse"
        field={$structureOptions.address1}
        bind:value={structure.address1}
        vertical />
      <ModelField
        type="text"
        label="Complément d’adresse"
        field={$structureOptions.address2}
        bind:value={structure.address2}
        vertical />
      <div class="flex flex-row justify-between gap-x-4">
        <div class="w-20">
          <ModelField
            type="text"
            label="Code postal"
            field={$structureOptions.postalCode}
            bind:value={structure.postalCode}
            vertical />
        </div>
        <div class="flex-auto">
          <ModelField
            type="text"
            label="Ville"
            field={$structureOptions.city}
            bind:value={structure.city}
            vertical />
        </div>
      </div>
      <div class="flex flex-row justify-between gap-x-4 ">
        <div class="flex-auto">
          <ModelField
            type="tel"
            label="Téléphone"
            field={$structureOptions.phone}
            bind:value={structure.phone}
            vertical />
        </div>

        <div class="flex-auto">
          <ModelField
            type="email"
            label="Courriel"
            field={$structureOptions.email}
            bind:value={structure.email}
            vertical />
        </div>
      </div>
      <ModelField
        type="url"
        label="Site web"
        field={$structureOptions.url}
        bind:value={structure.url}
        vertical />
      <ModelField
        type="textarea"
        label="Résumé"
        description="280 caractères maximum"
        placeholder="Décrivez brièvement votre structure"
        field={$structureOptions.shortDesc}
        bind:value={structure.shortDesc} />
      <ModelField
        type="richtext"
        label="Présentez votre structure"
        description="Présentation résumée des missions de votre structure"
        placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
        field={$structureOptions.fullDesc}
        bind:value={structure.fullDesc}
        vertical />

      <ModelField
        type="hidden"
        field={$structureOptions.cityCode}
        bind:value={structure.cityCode}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.ape}
        bind:value={structure.ape}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.longitude}
        bind:value={structure.longitude}
        vertical />
      <ModelField
        type="hidden"
        field={$structureOptions.latitude}
        bind:value={structure.latitude}
        vertical />

      <div class="border-b border-gray-01" />

      <div class="self-end">
        <ValidateButton {structure} />
      </div>
    </FieldSet>
  {/if}
{/if}
