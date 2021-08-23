<script>
  import Info from "./_info.svelte";
  import Box from "./_box.svelte";
  export let service;
</script>

<style>
  .infos {
    display: flex;
    flex-direction: column;
    margin-bottom: var(--s32);
    gap: var(--s8);
  }

  .list {
    display: flex;
    flex-direction: column;
    margin-top: var(--s20);
    margin-bottom: var(--s32);
    gap: var(--s8);
    list-style-position: inside;
    list-style-type: "– ";
  }

  .list li span {
    position: relative;
    left: var(--s8);
  }
</style>

<Box title="Les modalités du dispositif" --box-color="var(--col-magenta-cta)">
  <div class="infos">
    {#if service.isCumulative}
      <Info
        label="Cette offre de service est cumulable avec d’autres dispositifs"
        positiveMood />
    {:else}
      <Info
        label="Cette offre de service n’est pas cumulable avec d’autres dispositifs"
        negativeMood />
    {/if}

    {#if service.hasFee}
      <Info
        label="Frais à charge du bénéficiaire : {service.feeDetails}"
        negativeMood />
    {/if}
  </div>
  <div class="flex flex-row">
    <div class="flex-1">
      <h3>Critères d’admission</h3>
      <ul class="list">
        {#each service.accessConditionsDisplay as condition}
          <li><span>{condition}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>
    </div>
    <div class="flex-1">
      <h3>Public concerné</h3>
      <ul class="list">
        {#each service.concernedPublicDisplay as pub}
          <li><span>{pub}</span></li>
        {:else}
          <li><span>Tout le monde</span></li>
        {/each}
      </ul>
    </div>

    <div class="flex-1">
      <h3>Lieu de déroulement</h3>
      <ul class="list">
        {#each service.locationKindsDisplay as location}
          <li><span>{location}</span></li>
        {:else}
          <li><span>Non renseigné</span></li>
        {/each}
      </ul>
    </div>
  </div></Box>
