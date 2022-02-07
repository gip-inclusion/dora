<script>
  import { onMount } from "svelte";
  import SearchBySiret from "$lib/components/structures/search-by-siret.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Button from "$lib/components/button.svelte";

  import { arrowLeftSIcon } from "$lib/icons.js";
  import Toggle from "$lib/components/toggle.svelte";

  import { registrationInfo } from "./_store.js";
  import { getApiURL } from "$lib/utils/api.js";

  export let currentStep, siret;
  let establishment;

  let establishmentVisible = false;
  let hasCheckedConsent = false;

  function handleJoin() {
    $registrationInfo.siret = establishment.siret;
    $registrationInfo.isPoleEmploi = false;
    currentStep = 4;
  }

  async function searchSiret(q) {
    const sireneAPIUrl = `${getApiURL()}/search-siret/?siret=${encodeURIComponent(
      q
    )}`;
    const response = await fetch(sireneAPIUrl, {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json; version=1.0",
      },
    });
    if (response.ok) {
      const result = await response.json();
      console.log(result);
      return result;
    }
    return null;
  }

  onMount(async () => {
    if (siret) {
      establishment = await searchSiret(siret);
      if (establishment) {
        establishmentVisible = true;
      } else {
        siret = null;
      }
    }
  });

  $: console.log(siret);
</script>

<FieldSet
  title="Votre structure"
  description="Merci de renseigner le numéro SIRET de votre structure afin de l’identifier."
>
  {#if !siret}
    <SearchBySiret bind:establishment />
  {/if}
  {#if establishment && establishmentVisible}
    <div class="establishment-details">
      <h4 class="text-gray-text">{establishment.name}</h4>
      <div class="legend">{establishment.address1}</div>
      <div class="legend">{establishment.address2}</div>
      <div class="legend">
        {establishment.postalCode}
        {establishment.city}
      </div>
    </div>
    <div class="flex">
      <Toggle
        toggleYesText=""
        toggleNoText=""
        bind:checked={hasCheckedConsent}
      />
      <p class="legend">
        En cochant cette case, je déclare faire partie de la structure
        mentionnée ci-dessus et j’atteste connaître les risques encourus en cas
        de faux et d’usage de faux.
      </p>
    </div>
  {/if}

  <div class="flex flex-col items-start md:flex-row md:justify-between">
    <Button
      label="Retour"
      on:click={() => (currentStep = 1)}
      icon={arrowLeftSIcon}
      noPadding
      noBackground
      iconOnLeft
    />
    {#if !establishmentVisible}
      <Button
        label="Chercher la structure"
        disabled={!establishment}
        on:click={() => (establishmentVisible = true)}
      />
    {:else}
      <Button
        label="Adhérez à la structure"
        disabled={!hasCheckedConsent}
        on:click={handleJoin}
      />
    {/if}
  </div>
</FieldSet>

<style lang="postcss">
  .establishment-details {
    padding: var(--s24);
    border: 1px solid var(--col-gray-01);
  }
</style>
