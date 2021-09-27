<script>
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Modal from "$lib/components/modal.svelte";
  import { shortenString } from "$lib/utils";

  export let isOpen = false;
  export let service;

  function basename(path) {
    return shortenString(path.split("/").slice(-1)[0], 35);
  }
</script>

<style>
  .contents {
    display: block;
    width: 1264px;
    padding: var(--s32);
    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-md);
  }

  .box {
    padding: var(--s32) var(--s32) var(--s32);
    border: 3px solid var(--col-gray-dark);
    border-radius: var(--s8);
  }

  .action-line {
    display: flex;
    justify-content: flex-end;
    margin-top: var(--s24);
    gap: var(--s16);
  }

  .list {
    display: flex;
    flex-direction: column;
    margin: var(--s20) var(--s20) var(--s32) 0;
    color: var(--col-text);
    gap: var(--s8);
    list-style-position: inside;
    list-style-type: "– ";
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

<Modal bind:isOpen>
  <div class="contents">
    <h2 class="pb-2">Comment mobiliser ce service pour votre bénéficiaire</h2>
    <div class="box">
      <div class="flex flex-row">
        <div class="flex-1">
          <h3>Mobiliser la solution</h3>
          <ul class="list">
            {#each service.coachOrientationModesDisplay as mode}
              <li>
                <span>
                  {mode === "Autre (préciser)"
                    ? service.coachOrientationModesOther
                    : mode}
                </span>
              </li>
            {:else}
              <li><span>Non renseigné</span></li>
            {/each}
          </ul>
        </div>
        <div class="flex-1">
          <h3>Documents et justificatifs</h3>
          <ul class="list">
            {#each service.credentialsDisplay as creds}
              <li><span>{creds}</span></li>
            {:else}
              <li><span>Aucun</span></li>
            {/each}
          </ul>
          {#if service.forms.length || service.onlineForm}
            <div class="border-t border-gray-03 mx-5" />
          {/if}
          {#if service.forms.length}
            <ul class="list">
              {#each service.forms as form}
                <li>
                  <span>
                    <a target="_blank" rel="noopener nofollow" href={form}
                      >{basename(form)}</a>
                  </span>
                </li>
              {/each}
            </ul>
          {/if}
          {#if service.onlineForm}
            <ul class="list">
              <li>
                <span>
                  <a
                    target="_blank"
                    rel="noopener nofollow"
                    href={service.onlineForm}
                    >{shortenString(service.onlineForm, 35)}</a>
                </span>
              </li>
            </ul>
          {/if}
        </div>

        <div class="flex-1">
          <h3>Personne à contacter</h3>
          <ul class="list">
            {#if service.contactName}
              <h4 class="pb-2">{service.contactName}</h4>
            {/if}
            <p><strong>{service.structureInfo.name}</strong></p>
            <p class="text-sm pb-2">
              {service.structureInfo.address1}<br />
              {#if service.structureInfo.address2}{service.structureInfo
                  .address2}<br />{/if}
              {service.structureInfo.postalCode}
              {service.structureInfo.city}
            </p>
            {#if service.contactPhone}
              <p class="text-sm">
                <a href="tel:{service.contactPhone}">{service.contactPhone}</a>
              </p>
            {/if}
            {#if service.contactEmail}
              <p class="text-sm">
                <a href="mailto:{service.contactEmail}">
                  {service.contactEmail}
                </a>
              </p>
            {/if}
            {#if service.structureInfo.url}
              <p class="text-sm">
                <a
                  target="_blank"
                  rel="noopener nofollow"
                  href={service.structureInfo.url}>Voir leur site internet</a>
              </p>
            {/if}
          </ul>
        </div>
      </div>
    </div>
    {#if service.contactEmail}
      <div class="action-line">
        <Label label="Au clic, ouverture de votre client e-mail :" />
        <LinkButton
          label="Orientez votre bénéficiaire"
          to="mailto:{service.contactEmail}" />
      </div>
    {/if}
  </div>
</Modal>
