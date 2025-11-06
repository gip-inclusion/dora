<script lang="ts">
  import {
    consent,
    CONSENT_CONFIG,
    type ConsentChoices,
    type ConsentKey,
  } from "$lib/utils/consent.svelte";
  import CloseLineSystem from "svelte-remix/CloseLineSystem.svelte";
  import Button from "$lib/components/display/button.svelte";
  import DetailCard from "$lib/components/specialized/cookie-banner/detail-card.svelte";

  interface Props {
    handleSavePreferences: (consentChoices: ConsentChoices) => void;
    handleBackClick: () => void;
    handleAcceptAll: () => void;
    handleRejectAll: () => void;
  }

  let {
    handleSavePreferences,
    handleBackClick,
    handleAcceptAll,
    handleRejectAll,
  }: Props = $props();

  let consentChoices = $state({ ...consent.consentChoices });

  function toggleConsentByKey(key: ConsentKey) {
    consentChoices[key] = !consentChoices[key];
  }
</script>

<div class="p-s32 h-[580px] w-[792px]">
  <Button
    extraClass="absolute top-s16 right-s64"
    label="Fermer"
    onclick={handleBackClick}
    icon={CloseLineSystem}
    iconOnRight
    noBackground
    noPadding
  />
  <div class="h-[550px] overflow-y-scroll">
    <h2 class="mb-s32 mt-s16 text-[1.5rem]">Panneau de gestion des cookies</h2>
    <div class="mb-s16 pb-s8 flex justify-between border-b-1">
      <div class="justify-items flex flex-col">
        <p class="mb-s4 text-[1rem]">Préférences pour tous les services</p>
        <a
          class="text-magenta-cta underline"
          href="/politique-de-confidentialite"
          >Données personnelles et cookies</a
        >
      </div>
      <div class="gap-s16 flex">
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
</div>
<div class="mt-s32 mx-s32 flex justify-end">
  <Button
    label="Confirmer mes choix"
    onclick={() => handleSavePreferences(consentChoices)}
  />
</div>
