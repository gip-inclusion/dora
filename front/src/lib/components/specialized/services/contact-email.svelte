<script lang="ts">
  import type { Service, ShortService } from "$lib/types";
  import { CANONICAL_URL } from "$lib/env";
  import { mailSendLineIcon } from "$lib/icons";
  import { userInfo } from "$lib/utils/auth";

  export let service: Service | ShortService;
  export let preferred = false;
  const emailSubject = encodeURIComponent(
    `Candidature ${service.name} / Demande d’orientation`
  );
  const emailBody = encodeURIComponent(
    `
  Bonjour,

  Je vous contacte concernant l’offre ${
    service.name
  } sur dora.inclusion.beta.gouv.fr.
  ${CANONICAL_URL}/services/${service.slug}


  [Votre message ici]


  Cordialement,
  ${$userInfo?.fullName}
  [Votre affiliation]

  [Rappel des justificatifs à joindre:]

  ${service.credentialsDisplay
    ?.map((credential) => `- ${credential}`)
    .join("\n")}
  `.trim()
  );
</script>

<div>
  <a
    class="flex items-center break-all text-f16"
    class:font-bold={preferred}
    href="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      role="img"
      aria-label="Courriel"
    >
      {@html mailSendLineIcon}
    </span>
    {service.contactEmail}
  </a>
</div>
