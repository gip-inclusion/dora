<script>
  import { token, userInfo } from "$lib/auth";
  import Label from "$lib/components/label.svelte";
  import LinkButton from "$lib/components/link-button.svelte";
  import { PDF_SERVICE_URL, CANONICAL_URL } from "$lib/env";

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

<div class="mb-s24 rounded-md p-s24 shadow-md ">
  <h4>Justificatifs</h4>
  <ul class="mb-s24 list-inside list-disc text-f14">
    {#each service.credentialsDisplay as creds}
      <li><span>{creds}</span></li>
    {:else}
      <li><span>Aucun</span></li>
    {/each}
  </ul>

  {#if service.formsInfo.length}
    <h4>À compléter</h4>
    <ul class="mb-s24 list-inside list-disc text-f14">
      {#each service.formsInfo as form}
        <li>
          <span class="break-all">
            <a target="_blank" rel="noopener nofollow" href={form.url}
              >{form.name}</a
            >
          </span>
        </li>
      {/each}
    </ul>
  {/if}

  {#if showContact && service.contactName}
    <h4>Contact</h4>
    <p class="text-f14">
      {service.contactName}
      {#if service.contactPhone}
        <br />
        <a href="tel:{service.contactPhone}">{service.contactPhone}</a>
      {/if}
      {#if service.contactEmail}
        <br /><a href="mailto:{service.contactEmail}">{service.contactEmail}</a>
      {/if}
    </p>
  {:else}
    <div class="flex flex-col gap-s16 pb-s8">
      <Label
        label="Connectez-vous pour accéder aux informations de contact et mobiliser ce service pour votre bénéficiaire."
      />
    </div>
  {/if}

  {#if service.contactEmail && showContact}
    <div class="noprint">
      <LinkButton
        on:click={trackClick}
        label="Mobiliser le service"
        wFull
        to="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
      />
    </div>
  {/if}
</div>

<div class="noprint">
  {#if !service.isDraft}
    <LinkButton
      secondary
      wFull
      small
      noPadding
      label="Télécharger la page (.pdf)"
      to={pdfUrl}
      nofollow
    />
  {/if}
</div>
