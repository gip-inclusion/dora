<script>
  import { CANONICAL_URL } from "$lib/env.js";
  import { userInfo } from "$lib/auth.js";
  import { mailLineIcon } from "$lib/icons";

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
</script>

<div>
  <a
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
