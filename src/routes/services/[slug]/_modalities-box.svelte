<script>
  import Box from "./_box.svelte";
  export let service;
</script>

<Box title="Les modalités du dispositif" --box-color="blue">
  <div>
    {#if service.isCumulative}
      Cette offre de service est cumulable avec d’autres dispositifs
    {:else}
      Cette offre de service n’est pas cumulable avec d’autres dispositifs
    {/if}
  </div>

  <div>
    {#if service.hasFee}
      Frais à charge du bénéficiaire.
      {service.feeDetails}
    {:else}
      ### Pas de frais
    {/if}
  </div>
  <div class="flex flex-row">
    <div class="flex-1">
      <h3>Critères d’admission</h3>
      {#each service.accessConditionsDisplay as condition}
        {condition}<br />
      {:else}
        ## Aucune condition
      {/each}
    </div>
    <div class="flex-1">
      <h3>Public concerné</h3>
      {#each service.concernedPublicDisplay as pub}
        {pub}<br />
      {:else}
        ## Tout le monde
      {/each}
    </div>

    <div class="flex-1">
      <h3>Lieu de déroulement</h3>
      {#each service.locationKindsDisplay as location}
        {location}<br />
      {:else}
        ## Non renseigné
      {/each}
    </div>
  </div>
</Box>
