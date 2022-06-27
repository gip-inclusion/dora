<script>
  import { token, userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import Notice from "$lib/components/notice.svelte";
  import { PDF_SERVICE_URL, CANONICAL_URL } from "$lib/env";
  import { SERVICE_STATUSES } from "$lib/schemas/service";

  export let service;

  export let pagePath = `/services/${service.slug}`;
  export let pdfUrl = `${PDF_SERVICE_URL}/print/?page=${encodeURIComponent(
    pagePath
  )}&name=${service.slug}.pdf`;

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

  $: showContact = service?.isContactInfoPublic || $token;
</script>

{#if showContact}
  {#if service.contactName || service.contactPhone || service.contactEmail}
    <h4>Contact</h4>
    <p class="text-f14">
      {#if service.contactName}
        {service.contactName}
      {/if}
      {#if service.contactPhone}
        <br />
        <a href="tel:{service.contactPhone}">{service.contactPhone}</a>
      {/if}
      {#if service.contactEmail}
        <br /><a href="mailto:{service.contactEmail}">{service.contactEmail}</a>
      {/if}
    </p>
  {/if}
{:else}
  <div class="mb-s24">
    <Notice title="Connectez-vous"
      ><p class="text-f14">
        Accédez aux informations de contact et mobilisez ce service pour votre
        bénéficiaire.
      </p>
    </Notice>
  </div>
{/if}

{#if service.contactEmail && showContact}
  <div
    class="noprint"
    class:mb-s24={[
      SERVICE_STATUSES.draft,
      SERVICE_STATUSES.suggestion,
    ].includes(service.status)}
    class:mb-s12={service.status === SERVICE_STATUSES.published}
  >
    <LinkButton
      on:click={trackClick}
      label="Mobiliser le service"
      wFull
      to="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
    />
  </div>
{/if}

{#if service.status === SERVICE_STATUSES.published}
  <div class="noprint mb-s24">
    <LinkButton
      secondary
      wFull
      small
      label="Télécharger la page (.pdf)"
      to={pdfUrl}
      nofollow
    />
  </div>
{/if}
