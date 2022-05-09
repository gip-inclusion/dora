<script>
  import { addlinkToUrls } from "$lib/utils";
  export let service;
</script>

<div>
  <h2>Modalités</h2>
  <h4>Pour l'accompagnateur</h4>
  <ul class="mb-s24 list-inside list-disc">
    {#each service.coachOrientationModesDisplay as mode}
      <li class="break-words">
        {#if mode === "Autre (préciser)"}
          {@html addlinkToUrls(service.coachOrientationModesOther)}
        {:else}
          {mode}
        {/if}
      </li>
    {:else}
      <li><span>Non renseigné</span></li>
    {/each}
  </ul>

  <h4>Pour le bénéficiaire</h4>
  <ul class="mb-s24 list-inside list-disc">
    {#each service.beneficiariesAccessModesDisplay as mode}
      <li class="break-words">
        {#if mode === "Autre (préciser)"}
          {@html addlinkToUrls(service.beneficiariesAccessModesOther)}
        {:else}
          {mode}
        {/if}
      </li>
    {:else}
      <li><span>Non renseigné</span></li>
    {/each}
  </ul>

  {#if service.hasFee}
    <div class="mb-s24">
      <h4>Frais</h4>

      <p>{service.feeDetails}</p>
    </div>
  {/if}
</div>
