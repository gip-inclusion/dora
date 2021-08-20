<script>
  import Box from "./_box.svelte";
  export let service;
</script>

<Box title="Conditions d’accès pour le bénéficiaire" --box-color="black">
  <div class="flex flex-row">
    <div class="flex-1">
      <h3>Mobiliser la solution</h3>
      {#each service.beneficiariesAccessModesDisplay as mode}
        {mode}<br />
      {:else}
        ## Non renseigné
      {/each}
      {service.beneficiariesAccessModesOther}
    </div>

    <div class="flex-1">
      <h3>Pré-requis, compétences</h3>
      {#each service.requirementsDisplay as reqs}
        {reqs}<br />
      {:else}
        ## Aucun
      {/each}
    </div>

    <div class="flex-1">
      <h3>Documents et justificatifs</h3>
      {#each service.credentialsDisplay as creds}
        {creds}<br />
      {:else}
        ## Aucun
      {/each}
    </div>
  </div>
</Box>
