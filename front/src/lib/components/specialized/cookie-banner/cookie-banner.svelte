<script lang="ts">
  import {
    setConsentChoices,
    cookieBannerState,
  } from "$lib/utils/consent.svelte";
  import GeneralPanel from "$lib/components/specialized/cookie-banner/general-panel.svelte";
  import DetailPanel from "$lib/components/specialized/cookie-banner/detail-panel.svelte";

  let showDetails = $state(false);

  function closeBanner() {
    cookieBannerState.showBanner = false;
    showDetails = false;
  }

  function handleAcceptAll() {
    setConsentChoices({
      matomo: true,
      googleCSE: true,
      crisp: true,
    });
    closeBanner();
  }

  function handleRejectAll() {
    setConsentChoices({
      matomo: false,
      googleCSE: false,
      crisp: false,
    });
    closeBanner();
  }

  function handleSavePreferences(consentChoices) {
    setConsentChoices(consentChoices);
    closeBanner();
  }
</script>

{#if cookieBannerState.showBanner}
  <div
    class="mx-s16 md:mx-s0 bottom-s40 md:left-s40 p-s32 fixed z-[9999] bg-white shadow-md"
  >
    {#if !showDetails}
      <GeneralPanel
        {handleAcceptAll}
        {handleRejectAll}
        handlePersonalize={() => (showDetails = true)}
      />
    {:else}
      <DetailPanel
        {handleSavePreferences}
        {handleAcceptAll}
        {handleRejectAll}
        handleBackClick={() => (showDetails = false)}
      />
    {/if}
  </div>
{/if}
