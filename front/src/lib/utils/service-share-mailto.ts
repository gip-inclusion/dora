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
 * Retourne la liste des modes de mobilisation en remplaçant l'entrée
 * « Autre » par le texte libre saisi par la structure le cas échéant.
 */
function buildMobilizationModes(
  modes: ReadonlyArray<string> | null | undefined,
  modesDisplay: ReadonlyArray<string> | null | undefined,
  otherText: string | null | undefined
): string[] {
  const hasOther = modes?.includes("autre") ?? false;
  const items = (modesDisplay ?? []).filter(
    (label) => !hasOther || label.toLowerCase() !== "autre"
  );
  if (hasOther && otherText?.trim()) {
    items.push(otherText.trim());
  }
  return items;
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

  const beneficiaryModes = buildMobilizationModes(
    service.beneficiariesAccessModes,
    service.beneficiariesAccessModesDisplay,
    service.beneficiariesAccessModesOther
  );
  const professionalModes = buildMobilizationModes(
    service.coachOrientationModes,
    service.coachOrientationModesDisplay,
    service.coachOrientationModesOther
  );

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
    formatBulletList(beneficiaryModes),
    "",
    "Si vous êtes un professionnel :",
    formatBulletList(professionalModes),
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
