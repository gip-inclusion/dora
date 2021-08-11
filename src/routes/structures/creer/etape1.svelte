<script>
  import { structureCache, structureOptions } from "./_creation-store.js";

  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import FieldHelp from "$lib/components/forms/field-help.svelte";
  import Field from "$lib/components/forms/field.svelte";

  import ModelField from "$lib/components/forms/model-field.svelte";

  import CustomLayout from "./_custom-layout.svelte";

  import NavButtons from "./_nav.svelte";

  import SiretSearch from "./_siret_search.svelte";
  import CitySearch from "./_city_search.svelte";

  let selectedCity;

  $: console.log($structureOptions);
  $: console.log($structureCache);

  function handleCityChange(city) {
    console.log("handleCityChange");
    selectedCity = city;
    console.log(selectedCity);
  }

  function handleEstablishmentChange(establishment) {
    console.log("handleEstablishmentChange", establishment);
    $structureCache.siret = establishment.siret;
    $structureCache.name = establishment.name || establishment.parent;
    $structureCache.address1 = establishment.addr1;
    $structureCache.address2 = establishment.addr2;
    $structureCache.city = (
      (establishment.city || "") +
      " " +
      (establishment.distrib || "")
    ).trim();
    $structureCache.cityCode = establishment.citycode;
    $structureCache.postalCode = establishment.postcode;
    $structureCache.ape = establishment.ape;
    $structureCache.longitude = establishment.longitude;
    $structureCache.latitude = establishment.latitude;
  }
</script>

<CustomLayout>
  <svelte:fragment slot="content">
    {#if $structureOptions}
      <FieldSet
        title="Retrouvez votre structure"
        description="On peut récuperer automatiquement les informations importantes de votre structure via la base SIRENE. Saissisez votre département et le numéro SIRET pour commencer.">
        <Field label="Commune" vertical>
          <CitySearch
            slot="input"
            selectedCity
            placeholder="Saisissez le nom de votre ville"
            handleChange={handleCityChange} />
          <FieldHelp
            title="Récupération des données existantes"
            slot="helptext">
            <p>
              Pour faciliter l’étape de saisie, nous récupérons pour vous des
              données que l’État possède déjà. Une série d’éléments
              complémentaires vous seront demandés afin de réaliser et
              promouvoir un profil complet de votre structure. Pensez à mettre à
              jour régulièrement ces informations.
            </p>
          </FieldHelp>
        </Field>
        <Field label="Le nom de votre structure ou le numéro SIRET" vertical>
          <SiretSearch
            slot="input"
            selectedEstablishment
            {selectedCity}
            disabled={!selectedCity?.value?.properties?.citycode}
            handleChange={handleEstablishmentChange}
            placeholder="Commencez à saisir et choisissez dans la liste" />
        </Field>
      </FieldSet>

      {#if !$structureCache.siret}
        <FieldSet title="Présentez votre Structure">
          <ModelField
            type="text"
            field={$structureOptions.siret}
            disabled
            bind:value={$structureCache.siret}
            vertical />
          <ModelField
            type="text"
            label="Nom de la structure"
            field={$structureOptions.name}
            bind:value={$structureCache.name}
            vertical />
          <ModelField
            type="text"
            label="Adresse"
            field={$structureOptions.address1}
            bind:value={$structureCache.address1}
            vertical />
          <ModelField
            type="text"
            label="Complément d’adresse"
            field={$structureOptions.address2}
            bind:value={$structureCache.address2}
            vertical />

          <div class="flex flex-row gap-x-4 justify-between">
            <div class="w-20">
              <ModelField
                type="text"
                label="Code postal"
                field={$structureOptions.postalCode}
                bind:value={$structureCache.postalCode}
                vertical />
            </div>
            <div class="flex-auto">
              <ModelField
                type="text"
                label="Ville"
                field={$structureOptions.city}
                bind:value={$structureCache.city}
                vertical />
            </div>
          </div>
          <div class="flex flex-row gap-x-4 justify-between ">
            <div class="flex-auto">
              <ModelField
                type="tel"
                label="Téléphone"
                field={$structureOptions.phone}
                bind:value={$structureCache.phone}
                vertical />
            </div>

            <div class="flex-auto">
              <ModelField
                type="email"
                label="E-mail"
                field={$structureOptions.email}
                bind:value={$structureCache.email}
                vertical />
            </div>
          </div>
          <ModelField
            type="url"
            label="Site web"
            field={$structureOptions.url}
            bind:value={$structureCache.url}
            vertical />

          <ModelField
            type="text"
            label="Présentez votre structure"
            description="Présentation résumée des missions de votre structure"
            placeholder="Veuillez ajouter ici toute autre information que vous jugerez utile — concernant votre structure et ses spécificités."
            field={$structureOptions.shortDesc}
            bind:value={$structureCache.shortDesc}
            vertical />

          <ModelField
            type="hidden"
            field={$structureOptions.cityCode}
            bind:value={$structureCache.cityCode}
            vertical />

          <ModelField
            type="hidden"
            field={$structureOptions.ape}
            bind:value={$structureCache.ape}
            vertical />
          <ModelField
            type="hidden"
            field={$structureOptions.longitude}
            bind:value={$structureCache.longitude}
            vertical />
          <ModelField
            type="hidden"
            field={$structureOptions.latitude}
            bind:value={$structureCache.latitude}
            vertical />
        </FieldSet>
      {/if}
    {/if}
  </svelte:fragment>

  <svelte:fragment slot="navbar">
    {#if !$structureCache.siret}
      <NavButtons withValidate />
    {/if}
  </svelte:fragment>
</CustomLayout>
