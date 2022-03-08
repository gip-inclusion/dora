<script>
  import { page } from "$app/stores";
  import { token, userInfo } from "$lib/auth";

  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import Modal from "$lib/components/modal.svelte";
  import { CANONICAL_URL } from "$lib/env";
  import { mailIcon } from "$lib/icons";
  import { addlinkToUrls } from "$lib/utils";

  export let isOpen = false;
  export let service;

  $: showContact = service?.isContactInfoPublic || $token;

  const emailSubject = encodeURIComponent(
    `Candidature ${service.name} / Demande d'orientation`
  );
  const emailBody = encodeURIComponent(
    `
Bonjour,

Je vous contacte concernant l’offre ${
      service.name
    } sur dora.fabrique.social.gouv.fr.
${CANONICAL_URL}/services/${service.slug}


[Votre message ici]


Cordialement,
${$userInfo?.fullName}
[Votre affiliation]

[Rappel des justificatifs à joindre:]

${service.credentialsDisplay.map((s) => `- ${s}`).join("\n")}
`.trim()
  );

  function trackClick() {
    plausible("mobilisation-contact", {
      props: {
        service: service.name,
        slug: service.slug,
        structure: service.structureInfo.name,
        departement: service.department,
      },
    });
  }
</script>

<Modal bind:isOpen>
  <div class="modal-contents">
    <h2 class="pb-s16">Comment mobiliser ce service pour votre bénéficiaire</h2>
    <div class="box">
      <div class="flex flex-row flex-wrap gap-s24">
        <div class="flex-1">
          <h3>Mobiliser la solution</h3>
          <ul class="list">
            {#each service.coachOrientationModesDisplay as mode}
              <li>
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
            <div class="mx-s40 border-t border-gray-03" />
          {/if}
          {#if service.forms.length}
            <ul class="list">
              {#each service.forms as form}
                <li>
                  <span class="break-all">
                    <a target="_blank" rel="noopener nofollow" href={form}
                      >{form}</a
                    >
                  </span>
                </li>
              {/each}
            </ul>
          {/if}
          {#if service.onlineForm}
            <ul class="list">
              <li>
                <div>
                  <span class="break-all">
                    <a
                      target="_blank"
                      rel="noopener nofollow"
                      href={service.onlineForm}>{service.onlineForm}</a
                    >
                  </span>
                </div>
              </li>
            </ul>
          {/if}
        </div>

        <div class="flex-1">
          <h3>Personne à contacter</h3>
          <ul class="list">
            {#if showContact}
              {#if service.contactName}
                <h4 class="pb-s16">{service.contactName}</h4>
              {/if}
            {:else}
              <div class="flex flex-col gap-s16 pb-s8">
                <Label
                  label="Connectez-vous pour accéder aux informations de contact et mobiliser ce service pour votre bénéficiaire."
                />
                <LinkButton
                  label="Connexion"
                  to={`/auth/connexion?next=${encodeURIComponent(
                    $page.url.pathname
                  )}`}
                />
              </div>
            {/if}
            <p><strong>{service.structureInfo.name}</strong></p>
            <p class="pb-s16 text-f14">
              {service.structureInfo.address1}<br />
              {#if service.structureInfo.address2}{service.structureInfo
                  .address2}<br />{/if}
              {service.structureInfo.postalCode}
              {service.structureInfo.city}
            </p>
            {#if showContact}
              {#if service.contactPhone}
                <p class="text-f14">
                  <a href="tel:{service.contactPhone}">{service.contactPhone}</a
                  >
                </p>
              {/if}
              {#if service.contactEmail}
                <p class="break-all text-f14">
                  <a href="mailto:{service.contactEmail}">
                    {service.contactEmail}
                  </a>
                </p>
              {/if}
            {/if}
            {#if service.structureInfo.url}
              <!-- <p class="text-f14">
                <a
                  target="_blank"
                  rel="noopener nofollow"
                  href={service.structureInfo.url}>Voir leur site internet</a
                >
              </p> -->
            {/if}
          </ul>
        </div>
      </div>
    </div>
    {#if service.contactEmail && showContact}
      <div class="action-line">
        <Label label="Au clic, ouverture de votre client e-mail :" />
        <LinkButton
          on:click={trackClick}
          label="Faire une demande"
          to="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
          icon={mailIcon}
          iconOnRight
        />
      </div>
    {/if}
  </div>
</Modal>

<style lang="postcss">
  .modal-contents {
    @apply p-s16 md:p-s32;

    background-color: var(--col-white);
    border-radius: var(--s8);
    box-shadow: var(--shadow-md);
  }

  .box {
    @apply p-s16 md:p-s32;

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
    list-style-position: outside;
    list-style-type: "– ";
    position: relative;
    left: var(--s16);
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
