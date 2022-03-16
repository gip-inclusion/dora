<script>
  import Info from "./_info.svelte";
  import Box from "./_box.svelte";
  import { shortenString } from "$lib/utils";

  export let service;
</script>

<Box title="Les modalités" --box-color="var(--col-magenta-cta)">
  <div class="mb-s16">
    <strong>Lieu de diffusion : {service.diffusionZoneDetailsDisplay}</strong>
    {#if service.qpvOrZrr}
      (uniquement QPV + ZRR)
    {/if}
  </div>
  <div class="infos">
    {#if service.isCumulative}
      <Info
        label="Ce service est cumulable avec d’autres dispositifs"
        positiveMood
      />
    {:else}
      <Info
        label="Ce service n’est pas cumulable avec d’autres dispositifs"
        negativeMood
      />
    {/if}

    {#if service.hasFee}
      <Info label="Frais à charge du bénéficiaire : " negativeMood>
        <svelte:fragment slot="details">{service.feeDetails}</svelte:fragment>
      </Info>
    {/if}
  </div>
  <div class="flex flex-row flex-wrap gap-s24">
    <div class="grow">
      <h3>Critères d’admission</h3>
      <ul class="list">
        {#each service.accessConditionsDisplay as condition}
          <li><span>{condition}</span></li>
        {:else}
          <li><span>Aucun</span></li>
        {/each}
      </ul>
    </div>
    <div class="grow">
      <h3>Public concerné</h3>
      <ul class="list">
        {#each service.concernedPublicDisplay as pub}
          <li><span>{pub}</span></li>
        {:else}
          <li><span>Tout le monde</span></li>
        {/each}
      </ul>
    </div>

    <div class="grow">
      <h3>Lieu de déroulement</h3>

      {#if !service.locationKinds.length}
        Non renseigné
      {:else}
        {#if service.locationKinds.includes("en-presentiel")}
          <h4 class="pt-s16 pb-s8">En présentiel</h4>
          <p class="pb-s16 text-f14">
            {service.address1}<br />
            {#if service.address2}{service.address2}<br />{/if}
            {service.postalCode}
            {service.city}
          </p>
        {/if}
        {#if service.locationKinds.includes("a-distance")}
          <h4 class="pt-s16 pb-s8">À distance</h4>
          <p class="pb-s16 text-f14">
            <a target="_blank" rel="noopener nofollow" href={service.remoteUrl}
              >{shortenString(service.remoteUrl, 35)}</a
            >
          </p>
        {/if}
      {/if}
    </div>
  </div>
</Box>

<style lang="postcss">
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

  a {
    color: var(--col-magenta-cta);
    font-weight: bold;
  }
</style>
