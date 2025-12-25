<script lang="ts">
  import MailSendLineBusiness from "svelte-remix/MailSendLineBusiness.svelte";

  import { CANONICAL_URL } from "$lib/env";
  import type { Service, ShortService } from "$lib/types";
  import { userInfo } from "$lib/utils/auth";

  interface Props {
    service: Service | ShortService;
    preferred?: boolean;
  }

  let { service, preferred = false }: Props = $props();
  const emailSubject = encodeURIComponent(
    `Candidature ${service.name} / Demande d’orientation`
  );
  const emailBody = encodeURIComponent(
    `
  Bonjour,

  Je vous contacte concernant l’offre ${
    service.name
  } sur dora.inclusion.gouv.fr.
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
    class="text-f16 flex items-center break-all"
    class:font-bold={preferred}
    href="mailto:{service.contactEmail}?subject={emailSubject}&body={emailBody}"
  >
    <span
      class="mr-s8 h-s24 w-s24 fill-current"
      role="img"
      aria-label="Courriel"
    >
      <MailSendLineBusiness />
    </span>
    {service.contactEmail}
  </a>
</div>
