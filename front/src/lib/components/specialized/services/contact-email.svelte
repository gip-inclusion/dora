<script lang="ts">
  import { CANONICAL_URL } from "#lib/env.ts";
  import ContactEmailLink from "./contact-email-link.svelte";
  import type { Service, ShortService } from "#lib/types.ts";
  import { userInfo } from "#lib/utils/auth.ts";

  interface Props {
    service: Service | ShortService;
    email: string;
    preferred?: boolean;
  }

  let { service, email, preferred = false }: Props = $props();
  const emailSubject = $derived(
    encodeURIComponent(`Candidature ${service.name} / Demande d’orientation`)
  );
  const emailBody = $derived(
    encodeURIComponent(
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
    )
  );

  const mailtoHref = $derived(
    `mailto:${email}?subject=${emailSubject}&body=${emailBody}`
  );
</script>

<ContactEmailLink {email} {mailtoHref} {preferred} />
