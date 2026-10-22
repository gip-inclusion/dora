import { URL_HELP_SITE } from "#lib/consts.js";
import { CANONICAL_URL } from "#lib/env.js";
import type { Service } from "#lib/types.js";
import { getMobilisationModesDisplay } from "#lib/utils/service.js";

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

function buildMobilizationModes(service: Service): string {
  return formatBulletList(getMobilisationModesDisplay(service));
}

export function buildServiceShareMailto(
  service: Service,
  isDI = false
): string {
  const serviceUrl = `${CANONICAL_URL}/services/${isDI ? "di--" : ""}${service.slug}`;

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
    ...(service.publicsPrecisions?.trim()
      ? ["", service.publicsPrecisions.trim()]
      : []),
    "",
    "Comment mobiliser ce service :",
    "",
    buildMobilizationModes(service),
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
