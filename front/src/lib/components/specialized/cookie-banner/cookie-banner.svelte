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
  <div
    class="mx-s16 md:mx-s0 bottom-s40 md:left-s40 p-s32 fixed z-[9999] bg-white shadow-md"
  >
    {#if !cookieBannerState.showDetails}
      <GeneralPanel
        {handleAcceptAll}
        {handleRejectAll}
        handlePersonalize={() => (cookieBannerState.showDetails = true)}
      />
    {:else}
      <DetailPanel
        {handleSavePreferences}
        {handleAcceptAll}
        {handleRejectAll}
      />
    {/if}
  </div>
{/if}
