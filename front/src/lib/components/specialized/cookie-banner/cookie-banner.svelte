<script lang="ts">
  import {
    setConsentChoices,
    cookieBannerState,
    hideCookieBanner,
  } from "$lib/utils/consent.svelte";
  import GeneralPanel from "$lib/components/specialized/cookie-banner/general-panel.svelte";
  import DetailPanel from "$lib/components/specialized/cookie-banner/detail-panel.svelte";

  function handleAcceptAll() {
    setConsentChoices({
      matomo: true,
      googleCSE: true,
      crisp: true,
    });
    hideCookieBanner();
  }

  function handleRejectAll() {
    setConsentChoices({
      matomo: false,
      googleCSE: false,
      crisp: false,
    });
    hideCookieBanner();
  }

  function handleSavePreferences(consentChoices) {
    setConsentChoices(consentChoices);
    hideCookieBanner();
  }
</script>

{#if cookieBannerState.showBanner}
  {#if !cookieBannerState.showDetails}
    <GeneralPanel
      {handleAcceptAll}
      {handleRejectAll}
      handlePersonalize={() => (cookieBannerState.showDetails = true)}
    />
  {:else}
    <DetailPanel {handleSavePreferences} {handleAcceptAll} {handleRejectAll} />
  {/if}
{/if}
