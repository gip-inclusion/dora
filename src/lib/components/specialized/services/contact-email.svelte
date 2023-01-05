<script lang="ts">
  import { CANONICAL_URL } from "$lib/env";
  import { mailLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";
  import { trackMobilisationEmail } from "$lib/utils/plausible";

  export let service;
  export let preferred = false;
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
    trackMobilisationEmail(service);
  }
</script>

<div>
  <a
    on:click={trackClick}
    class="flex items-center text-f16"
    class:font-bold={preferred}
    href="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
  >
    <span class="mr-s8 h-s24 w-s24 text-gray-text" aria-label="E-mail">
      {@html mailLineIcon}
    </span>
    {service.contactEmail}
  </a>
</div>
