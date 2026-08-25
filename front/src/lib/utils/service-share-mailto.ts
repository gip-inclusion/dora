import { URL_HELP_SITE } from "$lib/consts";
import { CANONICAL_URL } from "$lib/env";
import type { Service } from "$lib/types";

function formatBulletList(
  items: ReadonlyArray<string> | null | undefined,
  fallback = "Non renseigné"
): string {
  const filtered = (items ?? []).map((item) => item?.trim()).filter(Boolean);
  if (filtered.length === 0) {
    return fallback;
  }
  return filtered.map((item) => `- ${item}`).join("\n");
}

/**
 * Construit une URL `mailto:` permettant à l'utilisateur de partager
 * une fiche service via son client de messagerie habituel.
 *
 * Aucun destinataire n'est pré-rempli : l'utilisateur le saisit dans son client.
 */
export function buildServiceShareMailto(
  service: Service,
  isDI = false
): string {
  const serviceUrl = `${CANONICAL_URL}/services/${isDI ? "di--" : ""}${service.slug}`;

  const modes = [...(service.mobilisationModesDisplay ?? [])];
  if (service.mobilisationDetails?.trim()) {
    modes.push(service.mobilisationDetails.trim());
  }
  const hasUsagers = !!service.mobilisableBy?.includes("usagers");
  const hasProfessionnels = !!service.mobilisableBy?.includes("professionnels");

  const subject = `On vous a recommandé une solution solidaire`;

  const lines: string[] = [
    "Bonjour,",
    "",
    "On vous a recommandé le service suivant :",
    "",
    service.structureInfo.name,
    service.name,
  ];
  if (service.addressLine?.trim()) {
    lines.push(service.addressLine.trim());
  }
  lines.push(
    "",
    "Le public concerné :",
    formatBulletList(
      service.publicsDisplay,
      service.publicsDisplay === null ? "Non renseigné" : "Tous publics"
    ),
    "",
    "Comment mobiliser ce service :",
    "",
    "Si vous êtes un particulier :",
    formatBulletList(hasUsagers ? modes : []),
    "",
    "Si vous êtes un professionnel :",
    formatBulletList(hasProfessionnels ? modes : []),
    "",
    `Consulter le service : ${serviceUrl}`,
    "",
    "À très bientôt,",
    "L’équipe DORA",
    "",
    `En cas de difficulté, n’hésitez pas à contacter le support de la plateforme DORA (${URL_HELP_SITE}) pour obtenir de l’aide.`
  );

  const body = lines.join("\n");

  return `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
