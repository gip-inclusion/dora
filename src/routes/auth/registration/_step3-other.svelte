<script>
  import SearchBySiret from "$lib/components/structures/search-by-siret.svelte";
  import FieldSet from "$lib/components/forms/fieldset.svelte";
  import Button from "$lib/components/button.svelte";

  import { arrowLeftSIcon } from "$lib/icons.js";
  import Toggle from "$lib/components/toggle.svelte";

  import { registrationInfo } from "./_store.js";

  export let currentStep;
  let establishment;

  let establishmentVisible = false;
  let hasCheckedConsent = false;

  function handleJoin() {
    $registrationInfo.siret = establishment.siret;
    currentStep = 4;
  }
</script>

<style>
  .establishment-details {
    padding: var(--s24);
    border: 1px solid var(--col-gray-01);
  }

  .establishment-details p {
    color: var(--col-text-alt2);
  }

  .toggle {
    display: flex;
  }

  .toggle p {
    color: var(--col-text);
    font-size: var(--f14);
  }
</style>

<FieldSet
  title="Votre structure"
  description="Merci de renseigner le numéro SIRET de votre structure afin de l’identifier."
>
  <SearchBySiret bind:establishment />
  {#if establishment && establishmentVisible}
    <div class="establishment-details">
      <h4>{establishment.name}</h4>
      <p>{establishment.address1}</p>
      <p>{establishment.address2}</p>
      <p>
        {establishment.postalCode}
        {establishment.city}
      </p>
    </div>
    <div class="toggle">
      <Toggle
        toggleYesText=""
        toggleNoText=""
        bind:checked={hasCheckedConsent}
      />
      <p>
        En cochant cette case je déclare faire partie de la structure mentionnée
        ci-dessus et je suis conscient•e des risques j’encours en cas de faux et
        d’usage de faux.
      </p>
    </div>
  {/if}

  <div class="flex flex-col items-start md:justify-between md:flex-row">
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
