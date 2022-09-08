<script>
  import { token, userInfo } from "$lib/auth";
  import LinkButton from "$lib/components/link-button.svelte";
  import { CANONICAL_URL } from "$lib/env";

  export let service;

  export let pagePath = `/services/${service.slug}`;

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

{#if service.contactEmail && showContact}
  <div class="noprint w-full sm:w-auto">
    <LinkButton
      on:click={trackClick}
      label="Mobiliser le service"
      wFull
      to="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
    />
  </div>
{/if}
