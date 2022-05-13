<script>
  export let service;
</script>

<div>
  <h2>Publics</h2>

  <h4>Profils</h4>
  <ul class="mb-s24 list-inside list-disc text-f14">
    {#each service.concernedPublicDisplay as pub}
      <li><span>{pub}</span></li>
    {:else}
      <li><span>Tout le monde</span></li>
    {/each}
  </ul>

  <h4>Critères</h4>
  <ul class="mb-s24 list-inside list-disc text-f14">
    {#each service.accessConditionsDisplay as condition}
      <li><span>{condition}</span></li>
    {:else}
      <li><span>Aucun</span></li>
    {/each}
    {#if service.qpvOrZrr}
      <li>uniquement QPV + ZRR</li>
    {/if}
  </ul>

  <h4>Pré-requis, compétences</h4>
  <ul class="mb-s24 list-inside list-disc text-f14">
    {#each service.requirementsDisplay as reqs}
      <li><span>{reqs}</span></li>
    {:else}
      <li><span>Aucun</span></li>
    {/each}
  </ul>
</div>
