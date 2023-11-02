<script lang="ts">
  import { browser } from "$app/environment";

  const CONSENT_COOKIE_NAME = "mtm_consent";
  const CONSENT_REMOVED_COOKIE_NAME = "mtm_consent_removed";

  function getCookie(cookieName: string) {
    const cookiePattern = new RegExp("(^|;)[ ]*" + cookieName + "=([^;]*)"),
      cookieMatch = cookiePattern.exec(document.cookie);
    return cookieMatch ? window.decodeURIComponent(cookieMatch[2]) : 0;
  }

  function setCookie(
    cookieName: string,
    value: string | number,
    msToExpire: number
  ) {
    const expiryDate = new Date();
    expiryDate.setTime(new Date().getTime() + msToExpire);
    document.cookie =
      cookieName +
      "=" +
      encodeURIComponent(value) +
      (msToExpire ? ";expires=" + expiryDate.toUTCString() : "") +
      ";path=" +
      "/" +
      (location.protocol === "https:" ? ";secure" : "") +
      ";SameSite=Lax";
    if (
      (!msToExpire || msToExpire >= 0) &&
      getCookie(cookieName) !== String(value)
    ) {
      console.log(
        "There was an error setting cookie `" +
          cookieName +
          "`. Please check domain and path."
      );
    }
  }

  function hasConsent() {
    const consentCookie = getCookie(CONSENT_COOKIE_NAME);
    const removedCookie = getCookie(CONSENT_REMOVED_COOKIE_NAME);
    if (!consentCookie && !removedCookie) {
      return true; // No cookies set, so opted in
    }
    if (removedCookie && consentCookie) {
      setCookie(CONSENT_COOKIE_NAME, "", -129600000);
      return false;
    }
    return consentCookie || consentCookie !== 0;
  }

  function consentGiven() {
    setCookie(CONSENT_REMOVED_COOKIE_NAME, "", -129600000);
    setCookie(CONSENT_COOKIE_NAME, new Date().getTime(), 946080000000);
  }

  function consentRevoked() {
    setCookie(CONSENT_COOKIE_NAME, "", -129600000);
    setCookie(CONSENT_REMOVED_COOKIE_NAME, new Date().getTime(), 946080000000);
  }

  let consent: boolean;
  let useTracker = true;

  if (browser) {
    consent = !!hasConsent();
  }
</script>

<p>
  DORA utilise également la solution de mesure d'audience
  <a href="https://matomo.org/" class="underline"> Matomo </a>

  en l'ayant configuré en mode « exempté », conformément aux
  <a
    href="https://www.cnil.fr/fr/solutions-pour-la-mesure-daudience"
    class="underline"
  >
    recommandations de la CNIL</a
  >. Elle ne nécessite donc pas le consentement des personnes concernées. Vous
  pouvez malgré tout vous opposer au suivi de votre navigation, en décochant la
  case ci-dessous.
</p>

{#if browser}
  <div>
    {#if !navigator?.cookieEnabled}
      <p>
        La fonctionnalité de désactivation du suivi nécessite que les cookies
        soient autorisés.
      </p>
    {:else if consent}
      {#if useTracker}
        <input
          on:click={() => {
            window._paq.push(["optUserOut"]);
            consent = false;
            useTracker = true;
          }}
          id="trackVisits"
          type="checkbox"
          checked
        />
      {:else}
        <input
          on:click={() => {
            consentRevoked();
            consent = false;
            useTracker = false;
          }}
          id="trackVisits"
          type="checkbox"
          checked
        />
      {/if}

      <label for="trackVisits"
        ><strong>
          Vous êtes suivi(e), de façon anonyme. Décochez cette case pour vous
          exclure du suivi.
        </strong>
      </label>
    {:else}
      {#if useTracker}
        <input
          on:click={() => {
            window._paq.push(["forgetUserOptOut"]);
            consent = true;
            useTracker = true;
          }}
          id="trackVisits"
          type="checkbox"
        />
      {:else}
        <input
          on:click={() => {
            consentGiven();
            consent = true;
            useTracker = false;
          }}
          id="trackVisits"
          type="checkbox"
        />
      {/if}
      <label for="trackVisits">
        <strong>
          Vous n'êtes actuellement pas suivi(e). Cochez cette case pour ne plus
          être exclu(e) du suivi.
        </strong>
      </label>
      <p class="mt-s8">
        Note : si vous nettoyez vos cookies et supprimez le cookie d'exclusion,
        ou bien si vous changez d'ordinateur et/ou de navigateur, il vous faudra
        de nouveau effectuer la procédure d'exclusion.
      </p>
    {/if}
  </div>
{/if}
