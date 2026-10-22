import { getApiURL } from "#lib/utils/api.ts";
import { getAnalyticsId } from "#lib/utils/stats.ts";
import { log } from "#lib/utils/logger.ts";
import { type Consent, CONSENT_VERSION } from "#lib/utils/consent.svelte.ts";

export async function sendConsentToAPI(
  consentChoices: Consent["consentChoices"]
) {
  try {
    await fetch(`${getApiURL()}/consent-record/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        consentChoices,
        consentVersion: CONSENT_VERSION,
        anonymousUserHash: getAnalyticsId(),
      }),
    });
  } catch (error) {
    log("Le consentement de l'utilisateur n'a pas été sauvegardé", error);
  }
}
