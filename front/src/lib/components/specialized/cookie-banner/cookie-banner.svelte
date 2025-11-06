<script module lang="ts">
  import {
    setConsentChoices,
    shouldShowCookieBanner,
  } from "$lib/utils/consent.svelte";
  import GeneralPanel from "$lib/components/specialized/cookie-banner/general-panel.svelte";
  import DetailPanel from "$lib/components/specialized/cookie-banner/detail-panel.svelte";

  import { onMount } from "svelte";

  let showBanner = $state(true);
  let showDetails = $state(true);

  // onMount(() => {
  //   showBanner = shouldShowCookieBanner();
  // });

  function handleAcceptAll() {
    setConsentChoices({
      matomo: true,
      googleCSE: true,
      crisp: true,
    });
    showBanner = false;
  }

  function handleRejectAll() {
    setConsentChoices({
      matomo: false,
      googleCSE: false,
      crisp: false,
    });
    showBanner = false;
  }

  function handleSavePreferences(consentChoices) {
    setConsentChoices(consentChoices);
    showBanner = false;
  }
</script>

{#if showBanner}
  <div class="bottom-s40 left-s40 p-s32 fixed z-[9999] bg-white shadow-md">
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
