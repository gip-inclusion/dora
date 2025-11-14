<script lang="ts">
  import {
    consent,
    CONSENT_CONFIG,
    type ConsentChoices,
    type ConsentKey,
    cookieBannerState,
    handleBackClick,
  } from "$lib/utils/consent.svelte";
  import CloseLineSystem from "svelte-remix/CloseLineSystem.svelte";
  import Button from "$lib/components/display/button.svelte";
  import DetailCard from "$lib/components/specialized/cookie-banner/detail-card.svelte";
  import Modal from "$lib/components/hoc/modal.svelte";

  interface Props {
    handleSavePreferences: (consentChoices: ConsentChoices) => void;
    handleAcceptAll: () => void;
    handleRejectAll: () => void;
  }

  let { handleSavePreferences, handleAcceptAll, handleRejectAll }: Props =
    $props();

  let consentChoices = $state({ ...consent.consentChoices });

  function toggleConsentByKey(key: ConsentKey) {
    consentChoices[key] = !consentChoices[key];
  }
</script>

<Modal
  width="medium"
  isOpen
  noPadding
  hideCloseButton
  hideTitle
  onClose={handleBackClick}
>
  <div class="p-s32 flex min-h-full min-w-full flex-col">
    <Button
      extraClass="self-end"
      label="Fermer"
      onclick={handleBackClick}
      icon={CloseLineSystem}
      iconOnRight
      noBackground
      noPadding
    />
    <div>
      <h2 class="mb-s32 mt-s16 text-f24">Panneau de gestion des cookies</h2>
      <div
        class="mb-s16 pb-s8 border-b-gray-02 flex flex-col justify-between border-b-1 md:flex-row"
      >
        <div class="justify-items pr-s16 mb-s8 flex flex-col md:mb-0">
          <p class="mb-s4 text-f16">Préférences pour tous les services</p>
          <a
            class="text-magenta-cta underline"
            href="/politique-de-confidentialite"
            onclick={() => {
              cookieBannerState.showDetails = false;
            }}>Données personnelles et cookies</a
          >
        </div>
        <div class="gap-s16 flex flex-col md:flex-row">
          <Button label="Tout accepter" onclick={handleAcceptAll} />
          <Button label="Tout refuser" secondary onclick={handleRejectAll} />
        </div>
      </div>

      <div class="mb-6">
        {#each Object.values(CONSENT_CONFIG) as categoryConfig}
          <DetailCard
            {categoryConfig}
            disabled={categoryConfig.consentKey === "required"}
            {toggleConsentByKey}
            value={consentChoices[categoryConfig.consentKey]}
          />
        {/each}
      </div>
    </div>
    <div class="mt-s32 flex justify-end">
      <Button
        label="Confirmer mes choix"
        onclick={() => handleSavePreferences(consentChoices)}
      />
    </div>
  </div>
</Modal>
