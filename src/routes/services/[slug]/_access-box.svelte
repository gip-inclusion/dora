<script>
  import Box from "./_box.svelte";
  export let service;
</script>

<style>
  .list {
    display: flex;
    flex-direction: column;
    margin-top: var(--s20);
    margin-bottom: var(--s32);
    color: var(--col-text);
    gap: var(--s8);
    list-style-position: outside;
    position: relative;
    left: var(--s16);
    list-style-type: "– ";
    max-width: 40ch;
  }

  .list li span {
    position: relative;
    left: var(--s8);
  }
</style>

<Box title="Conditions d’accès" --box-color="black">
  <div class="flex flex-row flex-wrap gap-s24">
    <div class="grow">
      <h3>Mobiliser ce service</h3>
      <ul class="list">
        {#each service.beneficiariesAccessModesDisplay as mode}
          <li>
            <span
              >{mode === "Autre (préciser)"
                ? service.beneficiariesAccessModesOther
                : mode}</span
            >
          </li>
        {:else}
          <li><span>Non renseigné</span></li>
        {/each}
      </ul>
    </div>

    <div class="grow">
      <h3>Pré-requis, compétences</h3>
      <ul class="list">
        {#each service.requirementsDisplay as reqs}
          <li><span>{reqs}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>
    </div>

    <div class="grow">
      <h3>Documents et justificatifs</h3>
      <ul class="list">
        {#each service.credentialsDisplay as creds}
          <li><span>{creds}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>
    </div>
  </div>
</Box>
